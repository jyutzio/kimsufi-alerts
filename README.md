# kimsufi-alerts

## Usage

```bash
git clone https://github.com/jyutzio/kimsufi-alerts.git
cd kimsufi-alerts/

# Rename example config file
mv kimsufi-alerts.ini.example kimsufi-alerts.ini

# Modify your config settings
nano kimsufi-alerts.ini

# Add script to run every 5min via crontab
crontab -e

# Add the following line
*/5 * * * * cd /absolute/dir/to/kimsufi-alerts && /usr/bin/python3 kimsufi-alerts.py

# You should now recieve an email anytime the state changes of the models specified in the config file.
```
