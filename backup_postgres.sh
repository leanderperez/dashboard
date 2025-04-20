#!/bin/bash

# Variables
DATABASE="forum"
USUARIO="leander"
CORREO="leanderperez@gmail.com"
FECHA=$(date +"%Y-%m-%d_%H-%M")
ARCHIVO_RESPALDO="$DATABASE-$FECHA.sql.gz"

SUBJECT="Respaldo de $DATABASE ($FECHA)"
BODY="Respaldo de $DATABASE adjunto."
ARCHIVO="$ARCHIVO_RESPALDO"
CORREO_DESTINO="$CORREO"

# Realizar respaldo
pg_dump -h localhost -U $USUARIO -Fc $DATABASE | gzip > $ARCHIVO_RESPALDO

# Enviar correo
# echo "Respaldo de $DATABASE adjunto." | mail -s "Respaldo de $DATABASE ($FECHA)" -a $ARCHIVO_RESPALDO $CORREO
echo "$BODY" | mutt -s "$SUBJECT" -a "$ARCHIVO" -- "$CORREO_DESTINO"

# Eliminar archivo de respaldo (opcional)
rm $ARCHIVO_RESPALDO