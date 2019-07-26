echo "Installing utilities"
sudo apt-get install -y screen

echo "Setting up git"
sudo apt-get install -y git
git config --global user.email jlapenna@gmail.com;
git config --global user.name "Joe LaPenna";

echo "Installing nodejs 12"
curl -sL https://deb.nodesource.com/setup_12.x | bash -
apt-get install -y nodejs
