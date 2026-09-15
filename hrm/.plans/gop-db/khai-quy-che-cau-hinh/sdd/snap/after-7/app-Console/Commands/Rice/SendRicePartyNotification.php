<?php

namespace App\Console\Commands\Rice;

use GuzzleHttp\Client;
use Illuminate\Console\Command;
use Illuminate\Support\Facades\Log;
use Modules\Rice\Entities\Setting\RiceSetting;
use Carbon\Carbon;
use Modules\Rice\Entities\RiceMenuDay\RiceMenuDay;

class SendRicePartyNotification extends Command
{
    protected $signature = 'rice:party-notify';
    protected $description = 'Gửi thông báo ăn liên hoan';

    public function handle()
    {
        $partyTimeSendBefore = RiceSetting::where('column_name', 'party_time_send_notification_before')
            ->value('column_value_integer') ?? 0;

        $today = Carbon::today('Asia/Ho_Chi_Minh');

        $expectedPartyDate = $today->copy()->addDays($partyTimeSendBefore);

        $partyMenu = RiceMenuDay::where('date', $expectedPartyDate->toDateString())
            ->whereNotNull('menu_party_id')
            ->first();

        if (!$partyMenu) {
            $this->info("Không tìm thấy thực đơn liên hoan cho ngày: {$expectedPartyDate->toDateString()}");
            Log::info("Không tìm thấy thực đơn liên hoan cho ngày: {$expectedPartyDate->toDateString()}");
            return;
        }

        $partyDate = $partyMenu->date;

        $domains = config('rice.register_domains');

        $client = new Client();

        foreach ($domains as $domain) {
            try {
                $response = $client->post("$domain/api/v1/rice/notification/planning-party", [
                    'json' => [
                        'date' => $partyDate,
                    ],
                ]);

                $statusCode = $response->getStatusCode();
                // $body = $response->getBody()->getContents();
                Log::info("Gửi thông báo liên hoan thành công, domain: $domain", [
                    'status' => $statusCode,
                    'domain' => $domain,
                ]);

                $this->info("Gửi thông báo liên hoan thành công, domain: $domain - Status: $statusCode");
            } catch (\Exception $e) {
                Log::error("Gửi thông báo liên hoan thất bại, domain: $domain", [
                    'error' => $e->getMessage(),
                    'domain' => $domain,
                ]);
                $this->error("Gửi thông báo liên hoan thất bại, domain: $domain: " . $e->getMessage());
            }
        }
    }
}
