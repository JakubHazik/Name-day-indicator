MAKEFLAGS += --silent
all:
	echo "For installation run: 'sudo make install'"
install:
	rm -rf /usr/local/name-day-indicator
	mkdir -p /usr/local/name-day-indicator/src
	cp ./src/* /usr/local/name-day-indicator/src
	cp startup.sh /usr/local/name-day-indicator/
	cp name-day-indicator.desktop /usr/share/applications/
	cp name-day-indicator.desktop ~/.config/autostart
	echo "Successfully installed!"
