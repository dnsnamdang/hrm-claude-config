<?php

namespace App\Console\Commands\Rice;

use GuzzleHttp\Client;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use Modules\Rice\Entities\RiceMenuDay\RiceMenuDay;

class SendRiceRegularNotification extends Command
{
    protected $signature = 'rice:regular-notify';
    protected $description = 'Gửi thông báo dự trù suất ăn';

    public function handle()
    {
        $tomorrow = now()->addDay()->toDateString();
        $menuDay = RiceMenuDay::where('date', $tomorrow)
            ->whereNotNull('menu_regular_id')->first();
        if (!$menuDay) {
            $this->info('Không có thực đơn cho ngày ' . $tomorrow);

            return;
        }
        $domains = config('rice.register_domains');

        $client = new Client();

        foreach ($domains as $domain) {
            try {
                $response = $client->post("$domain/api/v1/rice/notification/planning-regular", [
                    'json' => [
                        'date' => $tomorrow
                    ]
                ]);
                $statusCode = $response->getStatusCode();
                $body = $response->getBody()->getContents();

                Log::info("Gửi thông báo dự trù suất ăn thành công, domain: $domain", [
                    'status' => $statusCode,
                    'domain' => $domain
                ]);
            } catch (\Exception $e) {
                $this->error("Gửi thông báo dự trù suất ăn thất bại, domain: $domain, error: " . $e->getMessage());
            }
        }
    }
}
