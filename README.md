AWS Data Pipeline Lab

📌 Objetivo

Proyecto personal para practicar:
Infrastructure as Code con CloudFormation
Manejo de múltiples ambientes (dev/test/prod)
AWS CLI
Separación de templates y parámetros
Flujo estilo enterprise con Git

🏗 Arquitectura

Actualmente el stack crea:
S3 Bucket parametrizado por ambiente
(Después aquí agregaremos Glue, Step Functions, Secrets Manager, etc.)

📁 Estructura del Proyecto

aws-data-pipeline-lab/
│
├── iac/
│   ├── templates/
│   │   └── data-platform.yaml
│   └── parameters/
│       ├── dev.json
│       ├── test.json
│       └── prod.json
│
├── src/
├── tests/
├── .gitignore
└── README.md

📂 Descripción de Carpetas
iac/
Infrastructure as Code (CloudFormation).
Contiene la definición declarativa de los recursos AWS.

iac/templates/

Contiene los templates YAML de CloudFormation.
Ejemplo:
data-platform.yaml
Define los recursos AWS (S3, IAM, Glue, etc.).
Documentación oficial:
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-anatomy.html

iac/parameters/

Contiene los archivos JSON con valores por ambiente.
Separación entre:
Infraestructura (template)
Configuración (parameters)
Documentación oficial:
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/parameters-section-structure.html

src/
Código fuente de procesos (ej: Glue jobs, scripts Python, ETL).

tests/
Pruebas unitarias del código en src.

.gitignore

Evita versionar archivos sensibles o temporales.
Ejemplo:
credenciales
entornos virtuales
cache

⚙️ Configuración del Entorno

Instalar AWS CLI

Configurar credenciales:\
aws configure

Verificar conexión:
aws sts get-caller-identity

Documentación:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html

🚀 Cómo desplegar ambiente DEV
Desde la raíz del proyecto:

PowerShell:
aws cloudformation create-stack `
  --stack-name data-platform-dev `
  --template-body file://iac/templates/data-platform.yaml `
  --parameters file://iac/parameters/dev.json

Git Bash:
aws cloudformation create-stack \
  --stack-name data-platform-dev \
  --template-body file://iac/templates/data-platform.yaml \
  --parameters file://iac/parameters/dev.json


🌍 Manejo de Ambientes

Cada ambiente usa:
Un stack diferente
Un archivo de parámetros diferente

Ejemplo:
data-platform-dev
data-platform-test
data-platform-prod

Esto simula separación enterprise.