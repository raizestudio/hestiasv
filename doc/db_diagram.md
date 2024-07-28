

Table authentication.baseuser {
  id varchar(36) [pk]
  password varchar
  email varchar
  last_login datetime
  date_joined date
  is_superuser bool
  is_staff bool
  is_active bool
  is_deleted bool

  last_update datetime
  timestamp_deleted timestamp
  role int

  Note: 'Represente un user'
}

Table location.base_user_phonenumbers {
  id int [pk]
  user varchar(36) [ref: <> authentication.baseuser.id]
  phone_number int [ref: <> location.phonenumber.id]
}

Table authentication.baseuser_groups {
  id int [pk]
  baseuser_id varchar(36) [ref: <> authentication.baseuser.id]
  group_id int [ref: <> auth.group.id]

  Note: 'M2M'
}

Table authentication.baseuser_user_permissions {
  id int [pk]
  baseuser_id varchar(36) [ref: <> authentication.baseuser.id]
  permission_id int [ref: <> auth.permission.id]

  Note: 'M2M'
}

Table authentication.baseuser_streets {
  id int [pk]
  user varchar(36) [ref: - authentication.baseuser.id]
  adress int [ref: - location.adress.id]

  Note: 'M2M'
}

Table user.customer {
  id int [pk]
  user varchar(36) [ref: - authentication.baseuser.id]
  wallet int [ref: - financial.wallet.id]

  Note: 'Recherche une course'
}

Table user.pro {
  id int [pk]
  user varchar(36) [ref: - authentication.baseuser.id]

  Note: 'Propose une course'
}

Table location.position {
  id int [pk]
  coordinate int [pk]

  Note: 'Represente une position geographique'
}

Table location.adress {
  id int [pk]
  number int
  adress_type int [ref: > location.adress_type.id]
  name varchar(128)
  city int [ref: > location.city.id]

  Note: 'Represente une adresse'
}

Table location.adress_type {
  id int [pk]
  name varchar(128)
  name_short varchar(32)

  Note: 'Represente un type d\'adresse'
}

Table location.city {
  id int [pk]
  name varchar(128)
  department int [ref: > location.department.id]

  Note: 'Represente une ville'
}

Table location.department {
  id int [pk]
  name varchar(128)
  region int [ref: > location.region.id]

  Note: 'Represente un departement'
}

Table location.region {
  id int [pk]
  name varchar(128)
  country int [ref: > location.country.code]

  Note: 'Represente une region'
}

Table location.country {
  code int [pk]
  name varchar(128)

  Note: 'Represente un pays'
}

Table location.phonenumber {
  id int [pk]
  number int
  country int [ref: > location.country.code]
}

Table location.ride {
  id int [pk, increment]
  customer int [ref: > user.customer.id]
  pro int [ref: > user.pro.id]
  car int [ref: > material.car.id]
  departure datetime
  date_arrival datetime
  date_position_depart int [ref: - location.position.id]
  position_arrival int [ref: - location.position.id]
  distance double

  Note: 'Represente un trajet.'
}

Table location.ride_positions {
  id int [pk]
  ride int [ref: - location.ride.id]
  position int [ref: - location.position.id]

  Note: 'M2M'
}

Table core.history {
  id int [pk]

  origin_content_type int
  origin_id int
  origin GenericForeignKey

  action int

  target_content_type int
  target_id int
  target GenericForeignKey

  Note: 'Historique des actions dans l\'app'
}

Table notification.notification {
  id int [pk]

  recipient varchar(36)

  trigger_content_id int
  trigger_id int
  trigger GenericForeignKey

  action int [ref: > notification.notification_action.id]
  description text

  target_content_id int
  target_id int
  target GenericForeignKey

  Note: 'Représente une notification'
}

Table notification.notification_base_users {
  id int [pk]
  notification int [ref: <> notification.notification.id]
  user varchar [ref: <> authentication.baseuser.id]
}

Table notification.notification_action {
  id int [pk]
  name varchar(128)

  Note: 'Action d\'une notification'
}

Table material.brand {
  id int [pk]
  name varchar(128)

  Note: 'Marque de voiture'
}

Table material.model {
  id int [pk]
  name varchar(128)
  brand int [ref: > material.brand.id]
  type int [ref: > material.car_type.id]

  Note: 'Modéle de voiture'
}

Table material.car_type {
  id int [pk]
  name varchar(64)

  Note: 'Un type de voiture (suv, berline, ...)'
}
Table material.car {
  id varchar(128) [pk]
  model int [ref: < material.model.id]

  Note: "Represente un vehicule."
}

Table financial.quotation_customers {
  id int [pk]
  quotation int [ref: - financial.quotation.id]
  customer int [ref: - user.customer.id]

  Note: 'M2M'
}

Table financial.quotation_pros {
  id int [pk]
  quotation int [ref: - financial.quotation.id]
  pro int [ref: - user.pro.id]

  Note: 'M2M'
}

Table financial.quotation {
  id varchar(36) [pk]
  ride int [ref: < location.ride.id]

  Note: 'Represente un devis/planitfication trajet, est lié a un contrat si accepté'
}

Table financial.contract {
  id int [pk, increment]
  ride int [ref: - location.ride.id]
  price decimal(10, 2)
  date_paiement datetime
  payment varchar(36) [ref: - financial.payement.id]

  Note: "Represente un paiement"
}

Table financial.payement {
  id varchar(36) [pk]
  method int [ref: > financial.payment_method.id]
  processed_at timestamp

  Note: 'Represente un payement'
}

Table financial.payment_method {
  id int [pk]
}

Table financial.credit_card {
  id int [pk]
  number varchar(64)
  expires_at varchar
  card_validation_code int
}

Table financial.wallet {
  id int [pk]
  name varchar(128)
  card int [ref: > financial.credit_card.id]
}

Table security.contact {
  id int [pk]
  name varchar(128)
}

Table security.contact_base_users {
  id int [pk]
  user varchar(36) [ref: <> authentication.baseuser.id]
  contact int [ref: <> security.contact.id]
}
