# 作成手順

1. Messaging APIを作成する  

2. Cloud9を環境構築する  

3. git cloneする  
```
git clone https://github.com/mochan-tk/ldgq-online-handson-linebot.git  
```
4. 下記を実行し、python3.6を選択します。  
```
sudo update-alternatives --config python
```
5. 下記を実行し、モジュールをインストールします。  
```
cd ldgq-online-handson-linebot
sudo pip install -r requirements.txt  
```
6. 「.chalice/config.jsonファイル」ファイルを設定する   
・「LINEBOT_CHANNEL_ACCESS_TOKEN」、「LINEBOT_CHANNEL_SECRET」  
「1」で生成した「アクセストークン」と「Channel Secret」  

7. Cloud9の自動クレデンシャル設定を無効化にし、設定する  
```
aws configure  
```

8. Chaliceプロジェクトの作成、配置、デプロイ  
```
cd ~/environment/
chalice new-project line-bot

cd ~/environment/ldgq-online-handson-linebot
cp -p app.py ~/environment/line-bot
cp -p requirements.txt ~/environment/line-bot
cp -p .chalice/config.json ~/environment/line-bot/.chalice/  

cd  ~/environment/line-bot
chalice deploy  
```

9. Messaging APIのWebhookを設定する  
・Webhook送信  
する  
・Webhook URL  
https://xxx.execute-api.ap-northeast-1.amazonaws.com/api/webhook  

10. 動作確認をする  

11. Chaliceプロジェクトの削除(Lambda/API Gateway)  
```
cd ~/environment/line-bot/
chalice delete  
```
12. Cloud9環境の削除(下記アクセスして該当のプロジェクトをDelete)  
https://ap-northeast-1.console.aws.amazon.com/cloud9/home?region=ap-northeast-1#
