#!/bin/bash

# Variables
DATABASE="forum"
USUARIO="leander"
PASSWORD="Forum.2024"
CORREO="leanderperez@gmail.com"
FECHA=$(date +"%Y-%m-%d_%H-%M-%S")
ARCHIVO_RESPALDO="$DATABASE-$FECHA.sql.gz"

# Realizar respaldo
pg_dump -h localhost -U $USUARIO -w -Fc $DATABASE | gzip > $ARCHIVO_RESPALDO

# Enviar correo
echo "Respaldo de $DATABASE adjunto." | mail -s "Respaldo de $DATABASE ($FECHA)" -a $ARCHIVO_RESPALDO $CORREO

# Eliminar archivo de respaldo (opcional)
rm $ARCHIVO_RESPALDO