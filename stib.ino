#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <time.h>

const char* ssid = "WiFi-2.4-F302";
const char* wpd = "6CEcdAH6yg12";

// URLs
const char* urls[] = {
  "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22UZ-VUB%22&limit=100&refine=pointid%3A1755",
  "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GARE%20DE%20BERCHEM%22&limit=20&refine=pointid%3A1746",
  "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22ETANG%20NOIR%22&limit=20&refine=pointid%3A1746",
  "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GARE%20DU%20NORD%22&limit=100&refine=pointid%3A1768",
  "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GROOT-BIJGAARDEN%22&limit=100&refine=pointid%3A1680"
};

String getJson(const char* url);
void configureTime();
bool parseDate(const char* isoDate, struct tm* timeStruct);

void setup() {
  Serial.begin(115200);
  delay(1000);

  // Connexion au WiFi
  WiFi.begin(ssid, wpd);
  Serial.println("Connexion au WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.write('.');
  }
  Serial.println("\nConnecté au WiFi");

  // Configurer l'heure via NTP
  configureTime();

  // Traiter chaque URL
  for (int i = 0; i < 5; i++) {
    String response = getJson(urls[i]);

    if (response != "") {
      Serial.println("\nRéponse JSON pour URL: ");
      Serial.println(urls[i]);
      Serial.println(response);  // Affiche la réponse brute pour le débogage

      // Désérialiser le JSON principal
      DynamicJsonDocument root(2048);  // Augmente la taille si nécessaire
      DeserializationError error = deserializeJson(root, response);

      // Vérification des erreurs de désérialisation
      if (error) {
        Serial.print("Erreur de parsing JSON: ");
        Serial.println(error.c_str());
        return;
      }

      // Extraire les données du tableau "results"
      JsonArray results = root["results"].as<JsonArray>();
      if (results.size() > 0) {
        JsonObject result = results[0];

        // Extraire le "lineid" de la première entrée
        String lineid = result["lineid"].as<String>();
        Serial.print("LineID: ");
        Serial.println(lineid);

        // Récupérer la chaîne JSON du champ "passingtimes"
        String passingtimesStr = result["passingtimes"].as<String>();
        
        // Désérialiser la chaîne JSON à l'intérieur de "passingtimes"
        DynamicJsonDocument passingtimesDoc(2048);
        DeserializationError passingtimesError = deserializeJson(passingtimesDoc, passingtimesStr);

        if (passingtimesError) {
          Serial.print("Erreur de parsing du tableau 'passingtimes': ");
          Serial.println(passingtimesError.c_str());
          return;
        }

        // Extraire les informations de chaque passage
        JsonArray passingtimes = passingtimesDoc.as<JsonArray>();
        for (JsonObject passingtime : passingtimes) {
          const char* destination = passingtime["destination"]["fr"];
          const char* expectedArrivalTime = passingtime["expectedArrivalTime"];
          
          Serial.print("Destination: ");
          Serial.println(destination);
          Serial.print("Temps d'arrivée prévu: ");
          Serial.println(expectedArrivalTime);

          // Calculer la différence de temps
          struct tm expectedTime;
          if (parseDate(expectedArrivalTime, &expectedTime)) {
            // Calculer le temps restant
            time_t now = time(nullptr);  // Heure actuelle
            time_t arrival = mktime(&expectedTime);  // Heure d'arrivée
            double diff = difftime(arrival, now);  // Différence en secondes

            // Afficher la différence
            if (diff >= 0) {
              int minutes = diff / 60;  // Conversion en minutes
              Serial.print("Temps restant avant l'arrivée : ");
              Serial.print(minutes);
              Serial.println(" minutes");
            } else {
              Serial.println("Le transport est déjà passé.");
            }
          } else {
            Serial.println("Erreur de parsing de l'heure d'arrivée.");
          }
        }
      } else {
        Serial.println("Aucun enregistrement trouvé dans la réponse.");
      }
    } else {
      Serial.println("Erreur lors de la requête HTTP.");
    }
  }
}

void loop() {
  // Rien à faire dans la boucle
}

// Fonction pour récupérer les données JSON depuis l'URL
String getJson(const char* url) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Pas de connexion WiFi");
    return "";
  }

  HTTPClient http;
  http.begin(url);

  // Effectuer la requête HTTP
  int httpCode = http.GET();
  
  // Afficher le code de statut HTTP
  Serial.print("Code de statut HTTP : ");
  Serial.println(httpCode);

  // Vérifier si la requête a échoué
  if (httpCode <= 0) {
    Serial.println("Erreur lors de la requête HTTP");
    http.end();
    return "";
  }

  // Vérifier si la requête a réussi
  if (httpCode == HTTP_CODE_OK) {
    String payload = http.getString();
    http.end();
    return payload;
  }

  http.end();
  return "";
}

// Fonction pour configurer l'heure via NTP
void configureTime() {
  configTime(0, 3600, "pool.ntp.org"); // Configurer l'ESP32 pour obtenir l'heure à partir de NTP
  Serial.println("Synchronisation avec le serveur NTP...");
  
  // Attendre que l'heure soit synchronisée
  while (time(nullptr) < 1510644967) {
    delay(100);
  }
  Serial.println("Heure synchronisée.");
}

// Fonction pour parser une date ISO 8601
bool parseDate(const char* isoDate, struct tm* timeStruct) {
  char buffer[20];
  // Formater la chaîne pour l'analyser : yyyy-mm-ddTHH:MM:SS
  int ret = sscanf(isoDate, "%4d-%2d-%2dT%2d:%2d:%2d", 
                    &timeStruct->tm_year, &timeStruct->tm_mon, &timeStruct->tm_mday, 
                    &timeStruct->tm_hour, &timeStruct->tm_min, &timeStruct->tm_sec);

  if (ret != 6) {
    return false;  // Parsing échoué
  }
  
  // Ajuster l'année et le mois pour le format struct tm
  timeStruct->tm_year -= 1900;
  timeStruct->tm_mon -= 1;
  return true;
}
