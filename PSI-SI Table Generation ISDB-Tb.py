#ENCABEZADO DEL SCRIPT DE PHYTON, LIBRERÍAS Y VARIABLES UTILIZADAS
#!/usr/bin/env python
#coding: utf8
import os
from dvbobjects.PSI.PAT import* #Librerias de OpenCaster
from dvbobjects.PSI.NIT import* #Librerias de OpenCaster
from dvbobjects.PSI.SDT import* #Librerias de OpenCaster
from dvbobjects.PSI.PMT import* #Librerias de OpenCaster
from dvbobjects.SBTVD.Descriptors import* #Librerias de OpenCaster
tvd_ts_id             = 0x073b # ID de red.
tvd_orig_network_id   = 0x073b # ID de red original.
ts_freq               = 713    # Frecuencia de transmisión.
ts_remote_control_key = 0x05   # Tecla de control remoto virtual.
tvd_service_id_sd = 0xe760 # ID de servicio de TV Digital.
tvd_pmt_pid_sd    = 1031   # PID de la PMT del servicio.
#TABLA NIT, INFORMACIÓN DE LA RED
nit = network_information_section(
network_id = tvd_orig_network_id, # Valor asignado al ID de red original.
network_descriptor_loop = [
network_descriptor(network_name = "DETRITV",),# Nombre de la red
system_management_descriptor(
broadcasting_flag = 0, # Se realiza una transmisión libre
broadcasting_identifier = 3, # Se trata del valor del sistema ISDB-Tb
additional_broadcasting_identification = 0x01, # Identificación del servivio de radiodifusión
additional_identification_bytes = [],
)
],
transport_stream_loop = [
transport_stream_loop_item(
transport_stream_id = tvd_ts_id, # Asigna el valor del ID de red
original_network_id = tvd_orig_network_id, # Asigna el ID de red original
transport_descriptor_loop = [
service_list_descriptor(
dvb_service_descriptor_loop = [
service_descriptor_loop_item (
service_ID = tvd_service_id_sd, # Asigna el ID del servicio de TV Digital
service_type = 1, # Es el valor asignado al servicio de TV Digital
),
],
),
terrestrial_delivery_system_descriptor( #Define: modulación, intervalo de guarda, frecuencia.
area_code = 1341, # Indica el código de área
guard_interval = 0x00, # Indica el intervalo de guarda:1/32
transmission_mode = 0x02, # Indica el modo utilizado: Modo 3
frequencies = [
tds_frequency_item( freq=ts_freq ) #Asigna el valor de la frecuencia
],
),
partial_reception_descriptor ( #Define el listado de servicios de recepción parcial
service_ids = []
),
transport_stream_information_descriptor ( #Define características del TS a ser creado, tales como control remoto y servicios incluidos
remote_control_key_id = ts_remote_control_key, #Asigna el valor de la tecla de control remoto
ts_name = "DETRITV", # Asigna un nombre al archivo a generar
transmission_type_loop = [
transmission_type_loop_item(
transmission_type_info = 0x0F, #Define la transmisión en capas de acuerdo al proveedor
service_id_loop = [
service_id_loop_item(
service_id=tvd_service_id_sd #Asigna el valor del ID del servicio de TV
),
]
),
transmission_type_loop_item(
transmission_type_info = 0xAF, #Valor asignado para la transmisión en capas por el proveedor
service_id_loop = [],
),
],
)
],
),
],
version_number = 0, #Valor asignado a la versión de la tabla
section_number = 0, #Valor asignado a la sección de la tabla
last_section_number = 0, #Valor final asignado a la sección de la tabla
)
# TABLA SDT, DESCRIPCION DE SERVICIOS 
sdt = service_description_section( #Descripción del servicio de TV
transport_stream_id = tvd_ts_id, #Asigna el valor del ID de red
original_network_id = tvd_orig_network_id, #Asigna el valor del ID de red original
service_loop = [
service_loop_item(
service_ID = tvd_service_id_sd, #Asigna el valor de ID de servicio de TV Digital
EIT_schedule_flag          = 0, #Sin información del evento de radiodifusión
EIT_present_following_flag = 0, #Sin próximo evento de radiodifusión
running_status = 4, #El servicio se está ejecutando
free_CA_mode = 0, #El servicio no se encuentra codificado
service_descriptor_loop = [
service_descriptor(
service_type = 1, #Indica que se trata de un servicio de TV Digital
service_provider_name = "", #Nombre del proveedor de servicios
service_name = "DETRISD", # Indica el nombre asignado al servicio
),
],
),
],
version_number = 0, #Valor asignado a la versión de la tabla
section_number = 0, #Valor asignado a la sección de la tabla
last_section_number = 0, #Valor final asignado a la sección de la tabla
)
#TABLA PAT, información de los PID de las tablas PMP de la transmisión
pat = program_association_section(
transport_stream_id = tvd_ts_id, #Asigna el valor del ID de red
program_loop = [
program_loop_item(
program_number = 0, #Valor de programa requerido en la tabla NIT
PID = 16, # Identificador de la tabla NIT
),
program_loop_item(
program_number = tvd_service_id_sd, #Asigna el ID del servicio de TV
PID = tvd_pmt_pid_sd, #Es valor del PID del servicio de la tabla PMT
),
],
version_number = 0, #Valor asignado a la versión de la tabla
section_number = 0, #Valor asignado a la sección de la tabla
last_section_number = 0, #Valor final asignado a la sección de la tabla
)
#TABLA PMT, contiene los PID de audio y video, además la sincronización 
pmt_sd = program_map_section(
program_number = tvd_service_id_sd, #Asigna el ID de servicio de TV
PCR_PID = 2068, #Define el PID de la información de video
program_info_descriptor_loop = [],
stream_loop = [
stream_loop_item(
stream_type = 2, #Tipo de stream mpeg2 video 
elementary_PID = 2068, #Asigna el PID de la información de video 
element_info_descriptor_loop = [
]
),
stream_loop_item(
stream_type = 3, #Tipo de stream mpeg2 audio
elementary_PID = 2078, #Define el PID de la información de audio
element_info_descriptor_loop = []
),
],
version_number = 0, #Valor asignado a la versión de la tabla
section_number = 0, #Valor asignado a la sección de la tabla
last_section_number = 0, #Valor final asignado a la sección de la tabla
)
#CODIGO PARA GENERAR LOS ARCHIVOS .TS DE LAS TABLAS
out = open("./nit.sec", "wb") #Generación de la sección de la tabla NIT
out.write(nit.pack())
out.close()
os.system("sec2ts 16 < ./nit.sec > ./nit.ts") #Conversión de sección a TS de la tabla NIT
out = open("./pat.sec", "wb") #Generación de la sección de la tabla PAT
out.write(pat.pack())
out.close()
os.system("sec2ts 0 < ./pat.sec > ./pat.ts") #Conversión de sección a TS de la tabla PAT
out = open("./sdt.sec", "wb") #Generación de la sección de la tabla SDT
out.write(sdt.pack())
out.close()
os.system("sec2ts 17 < ./sdt.sec > ./sdt.ts") #Conversión de sección a TS de la tabla SDT
out = open("./pmt_sd.sec", "wb") #Generación de la sección de la PMT
out.write(pmt_sd.pack())
out.close()
os.system("sec2ts " + str(tvd_pmt_pid_sd) + " < ./pmt_sd.sec > ./pmt_sd.ts") #Conversión de sección a TS utilizando el PID de la PMT
