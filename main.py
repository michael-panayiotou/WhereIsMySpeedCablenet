import speedtest
import twitter
import configparser


def to_mbps(b):
    return b/1000000

# Parse twitter login configuration file
config = configparser.ConfigParser()
config.read('twitter_login.cfg')
config.sections()
c_key = config['twitter_login']['consumer_key']
c_secret = config['twitter_login']['consumer_secret']
t_key = config['twitter_login']['access_token_key']
t_secret = config['twitter_login']['access_token_secret']

# Specify server that we want to run speed test
# Cablenet has a server in Larnaca with ID: 2246
# We are going to use this one in order to have
# an accurate measurment
servers = [2246]

speed_measurement = speedtest.Speedtest()
speed_measurement.get_servers(servers)
speed_measurement.get_best_server()
print("Download Measurement")
speed_measurement.download()
print("Upload Measurement")
speed_measurement.upload()

print("Download: %.2f Mbps" % to_mbps(speed_measurement.results.download))
print("Upload: %.2f Mbps" % to_mbps(speed_measurement.results.upload))

api = twitter.Api(consumer_key=c_key,
                  consumer_secret=c_secret,
                  access_token_key=t_key,
                  access_token_secret=t_secret)

if to_mbps(speed_measurement.results.download) < 40:
    status = '😡Hey @CablenetCyprus, why do I get DL:%.1fMbps | UL:%.1fMbps ' \
                  'when I pay for 50Mbps? by speedtest.net|Server=Larnaca #PurpleWorld' \
                  % (to_mbps(speed_measurement.results.download),
                     to_mbps(speed_measurement.results.upload))

    update_status = api.PostUpdate(status,verify_status_length=False)
    print(update_status.text)
else:
    print("speed is okay")