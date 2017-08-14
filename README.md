# Kiririn

Kiririn is a natural language processing Telegram Bot with only FOSS components
targeted for Weeaboos and Anime/Manga fans alike.

But, it's not just limited for that, Thanks to how flexible [rasa][rasa] is
you can fork this bot and fit it to your own needs.

## How to setup

1. You need to setup a working environment where Rasa can run, our configuration
   uses MITIE and sk-learn because it's the fastest and most efficient one so
   far.
2. Install the requirements by running `pip install -r requirements.txt`.
3. Make a new configuration file based on the example and set the variables
   accordingly. You can start by running `cp config.ini.example config.ini`.
4. Train the data by running `./run_kiririn train`.
5. (Optional) Test the models by running `./run_kiririn parse <text>`.
6. Start the bot by running `./run_kiririn start`

## Contribute

We welcome contributions and Pull requests, here's a list of what you can do:

1. Extend the data set with more examples.
2. Suggest features on the issue tracker.
3. Report bugs on the issue tracker.
4. Do the issues yourself and submit a patch ;).

## License

Kiririn is licensed under the OpenBSD modified ISC License. Feel free to fork it
and fit it to your needs.

[rasa]: https://rasa.ai
