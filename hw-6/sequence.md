sequenceDiagram

participant User
participant Gateway
participant Broker
participant Auth Service
participant Order Service
participant Billing Service
participant Notification Service

User->>Gateway: POST /auth/register
activate Gateway
Note right of Gateway: RegisterUser
Gateway->>Broker: publish
activate Broker
Broker-->>Auth Service: consume
deactivate Broker
activate Auth Service
Auth Service->>Broker: publish
activate Broker
deactivate Auth Service
Note left of Auth Service: UserCreated
Broker-->>Gateway: consume
Gateway-->>User: 200 response
deactivate Gateway

Broker-->>Billing Service: consume
activate Billing Service
deactivate Billing Service

Broker-->>Notification Service: consume
deactivate Broker
activate Notification Service
Notification Service->>Auth Service: GET /users/info
activate Auth Service
Auth Service-->>Notification Service: response UserInfo
deactivate Auth Service
Notification Service->>Notification Service: send*
deactivate Notification Service

User->>Gateway: POST /order/create
activate Gateway
Note right of Gateway: CreateOrder
Gateway->>Broker: publish
activate Broker
Broker-->>Order Service: consume
deactivate Broker
activate Order Service
Order Service->>Broker: publish
activate Broker
Broker-->>Gateway: consume
Gateway-->>User: 201 created
deactivate Gateway

Note left of Order Service: AddPayTransaction
Broker-->>Billing Service: consume
deactivate Broker

activate Billing Service
Billing Service->>Broker: publish
deactivate Billing Service

activate Broker
Note right of Order Service: AddPayTransactionResponse
Broker-->>Order Service: consume
deactivate Broker

Order Service->>Broker: publish
deactivate Order Service
activate Broker
Note left of Order Service: SendEmail

Broker-->>Notification Service: consume
deactivate Broker

activate Notification Service
Notification Service->>Notification Service: send*
deactivate Notification Service