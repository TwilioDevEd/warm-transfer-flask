# Warm Transfer: Transfer support calls from one agent to another using Flask
![Flask](https://github.com/TwilioDevEd/warm-transfer-flask/workflows/Flask/badge.svg)

## Local development

This project is built using the [Flask](http://flask.pocoo.org/) web framework.

1. Clone this repository and `cd` into it.

1. Create and activate a new python3 virtual environment.

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

1. Install the requirements.

   ```bash
   pip install -r requirements.txt
   ```

1. Copy the sample configuration file and edit it to match your configuration.

   ```bash
   cp .env.example .env
   ```

   Twilio API credentials can be found [here](https://www.twilio.com/console) 
   and find you can create a REST API Key [here](https://www.twilio.com/console/project/api-keys).
   If using the twilio CLI you can run:
   
   ```bash
   twilio api:core:keys:create --friendly-name=worm-transfer -o json
   ```
   
1. Run the migrations.

   Our app uses SQLite, so you probably will not need to install additional software.
   
   ```bash
   python manage.py db upgrade
   ```

1. Expose your application to the wider internet using ngrok.

   To actually forward incoming calls, your development server will need to be publicly accessible.
   [We recommend using ngrok to solve this problem](https://www.twilio.com/blog/2015/09/6-awesome-reasons-to-use-ngrok-when-testing-webhooks.html).


   ```bash
   ngrok http 5000
   ```

   Once you have started ngrok, the public accessible URL will look like this:
   
   ```
   https://<your-ngrok-id>.ngrok.io/
   ```

1. Start the development server.

   ```bash
   python manage.py runserver
   ```

1. Configure Twilio to call your webhooks.

   You will also need to configure Twilio to call your application when calls are received on your `TWILIO_NUMBER`. The voice URL should look something like this:
   
   ```
   http://<your-ngrok-id>.ngrok.io/conference/connect/client
   ```

   ![Configure Voice](http://howtodocs.s3.amazonaws.com/twilio-number-config-all-med.gif)


That's it!


## How to Demo

1. Navigate to `https://<ngrok_subdomain>.ngrok.io` in two different
   browser tabs or windows.

   **Notes:**
   * Remember to use your SSL enabled ngrok URL `https`.
   Failing to do this won't allow you to receive incoming calls.

   * The application has been tested with [Chrome](https://www.google.com/chrome/)
   and [Firefox](https://firefox.com). Safari is not supported at the moment.

1. In one window/tab click `Connect as Agent 1` and in the other one click
   `Connect as Agent 2`. Now both agents are waiting for an incoming call.

1. Dial your [Twilio Number](https://www.twilio.com/user/account/phone-numbers/incoming) to start a call with `Agent 1`. Your `TWILIO_NUMBER`
   environment variable was set when configuring the application to run.

1. When `Agent 1` answers the call from the client, he/she can dial `Agent 2` in
   by clicking on the `Dial agent 2 in` button.

1. Once `Agent 2` answers the call all three participants will have joined the same
   call. After that, `Agent 1` can drop the call and leave both the client and `Agent 2`
   having a pleasant talk.

## Meta

* No warranty expressed or implied. Software is as is. Diggity.
* [MIT License](LICENSE)
* Lovingly crafted by Twilio Developer Education.
