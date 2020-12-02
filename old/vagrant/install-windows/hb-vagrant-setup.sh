#get rid of warnings about updating
#pipe any error messages into dev/null
rm /etc/update-motd.d/90* 2> /dev/null
rm /etc/update-motd.d/91* 2> /dev/null

#set up postgres for vagrant
sudo -u postgres createuser vagrant -s
sudo -u postgres createdb vagrant
sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/10/main/postgresql.conf
echo "host    all    all    10.0.0.0/16    trust" >> /etc/postgresql/10/main/pg_hba.conf
/etc/init.d/postgresql restart

sudo curl -s https://fellowship.hackbrightacademy.com/materials/tools/hbget-remote\
  --output /usr/local/bin/hbget
sudo chmod +x /usr/local/bin/hbget

# Set git name and author to Hackbright Student
git config --global user.name "Hackbright Student"
git config --global user.email "student@hackbrightacademy.com"

#print success message
echo
echo
echo "***************************************"
echo "HACKBRIGHT VAGRANT SET UP SUCCESSFULLY!"
echo "***************************************"
echo
echo
