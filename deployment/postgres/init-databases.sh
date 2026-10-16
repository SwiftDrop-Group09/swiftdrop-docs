#!/bin/sh
set -eu
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres   -v identity_password="$IDENTITY_DB_PASSWORD"   -v delivery_password="$DELIVERY_DB_PASSWORD"   -v merchant_password="$MERCHANT_DB_PASSWORD"   -v notifications_password="$NOTIFICATIONS_DB_PASSWORD" <<'SQL'
CREATE ROLE identity_app LOGIN PASSWORD :'identity_password';
CREATE ROLE delivery_app LOGIN PASSWORD :'delivery_password';
CREATE ROLE merchant_app LOGIN PASSWORD :'merchant_password';
CREATE ROLE notifications_app LOGIN PASSWORD :'notifications_password';
CREATE DATABASE swiftdrop_identity OWNER identity_app;
CREATE DATABASE swiftdrop_delivery OWNER delivery_app;
CREATE DATABASE swiftdrop_merchant OWNER merchant_app;
CREATE DATABASE swiftdrop_notifications OWNER notifications_app;
REVOKE ALL ON DATABASE swiftdrop_identity FROM PUBLIC;
REVOKE ALL ON DATABASE swiftdrop_delivery FROM PUBLIC;
REVOKE ALL ON DATABASE swiftdrop_merchant FROM PUBLIC;
REVOKE ALL ON DATABASE swiftdrop_notifications FROM PUBLIC;
SQL
for db in swiftdrop_identity swiftdrop_delivery swiftdrop_merchant swiftdrop_notifications; do
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$db"     -c 'REVOKE CREATE ON SCHEMA public FROM PUBLIC;'
done
