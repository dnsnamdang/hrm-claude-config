<?php

namespace App\Console\Commands\Rice;

use GuzzleHttp\Client;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use Modules\Rice\Entities\RiceMenuDay\RiceMenuDay;

class SendRiceRegularCloseNotification extends Command
{
    protected $signature = 'rice:regular-close-notify';
    protected $description = 'Gửi thông báo chốt suất ăn';

    public function handle()
    {
        $today = now()->toDateString();
        $menuDay = RiceMenuDay::where('date', $today)
            ->whereNotNull('menu_regular_id')->first();
        if (!$menuDay) {
            $this->info('Không có thực đơn cho ngày ' . $today);
            Log::info('Không có thực đơn cho ngày ' . $today);

            return;
        }
        $domains = config('rice.register_domains');
        $client = new Client();

        foreach ($domains as $domain) {
            try {
                $response = $client->post("$domain/api/v1/rice/notification/close-regular", [
                    'json' => [
                        'date' => $today
                    ]
                ]);
                $statusCode = $response->getStatusCode();
                $body = $response->getBody()->getContents();

                Log::info("Gửi thông báo chốt suất ăn thành công, domain: $domain", [
                    'status' => $statusCode,
                    'domain' => $domain
                ]);
            } catch (\Exception $e) {
                $this->error("Gửi thông báo chốt suất ăn thất bại, domain: $domain, error: " . $e->getMessage());
            }
        }
    }
}
