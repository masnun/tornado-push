<?php
/**
 * Author: Abu Ashraf Masnun
 * URL: http://masnun.me
 */

function getUserAuthToken($apiUrl, $secretKey, $username, $isMod)
{
    $data = "secret_key={$secretKey}&username={$username}&mod={$isMod}";

    $ch = curl_init($apiUrl);
    curl_setopt($ch, CURLOPT_POST, TRUE);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, TRUE);
    $response = curl_exec($ch);

    //var_dump($response);

    if ($response) {
        $authResponse = json_decode($response);
        if ($authResponse->status == 'ok') {
            return $authResponse->token;
        } else {
            return FALSE;
        }

    }
}