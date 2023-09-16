import sklearn
import requests
import json
import time
import asyncio
import telegram  # Asegúrate de instalar la biblioteca 'python-telegram-bot' si no lo has hecho.

# Configuración de Telegram
bot_token = '6474281726:AAHfE_XSGlLB5HhNQlWzNOIziM9IZvTFtmE'
chat_id = '-4094203781'

bot = telegram.Bot(token=bot_token)

# URL y datos JSON de entrada
url = 'https://api.consignee.gls-spain.es/api/v3/expeditions/find'
data = {
    "find": {
        "reference": "861579805",
        "destination": {
            "address": {
                "postalCode": "18001"
            }
        }
    }
}



# Función para enviar notificaciones a Telegram
async def send_telegram_notification(message):
    await bot.send_message(chat_id=chat_id, text=message)

# Función para verificar los cambios de estado
async def check_status():
    response = requests.post(url, json=data)
    if response.status_code == 200:
        response_data = response.json()
        
        #print(response_data)
        tracking = response_data.get('found', {}).get('tracking', [])
        
        # Compara los cambios de estado con el último estado registrado
        if 'last_tracking_step' in globals():
            new_tracking_step = tracking[0]
           
            
            if new_tracking_step !=  globals()['last_tracking_step']:
                # Ha habido un cambio de estado
                
                await send_telegram_notification(f'Cambio de estado: {new_tracking_step}')
                
        
        # Actualiza el último estado registrado
        last_tracking_step_code = tracking[0]
        globals()['last_tracking_step'] = last_tracking_step_code
        
        await send_telegram_notification(f'Estado actual: {last_tracking_step_code}')
    else:
        await send_telegram_notification(f'Error al obtener el estado: {response.status_code}')

# Ejecuta la verificación de estado cada X segundos (por ejemplo, cada 1 hora)
async def main():
    while True:
        await check_status()
        await asyncio.sleep(900)
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
