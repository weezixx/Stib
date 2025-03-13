#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <time.h>

const char* ssid = "WiFi-2.4-F302";
const char* wpd = "6CEcdAH6yg12";

const char* key = "736270cebb4e2191d31a70d74d7a9a782b6c747f087cb64eb01c2b62";

// URLs
const char* urls[] = {
  "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22UZ-VUB%22&limit=100&refine=pointid%3A1755&apikey=736270cebb4e2191d31a70d74d7a9a782b6c747f087cb64eb01c2b62",
  "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GARE%20DE%20BERCHEM%22&limit=20&refine=pointid%3A1746&apikey=736270cebb4e2191d31a70d74d7a9a782b6c747f087cb64eb01c2b62",
  "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22ETANG%20NOIR%22&limit=20&refine=pointid%3A1746&apikey=736270cebb4e2191d31a70d74d7a9a782b6c747f087cb64eb01c2b62",
  "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GARE%20DU%20NORD%22&limit=100&refine=pointid%3A1768&apikey=736270cebb4e2191d31a70d74d7a9a782b6c747f087cb64eb01c2b62",
  "https://data.stib-mivb.be/api/explore/v2.1/catalog/datasets/waiting-time-rt-production/records?where=%22GROOT-BIJGAARDEN%22&limit=100&refine=pointid%3A1680&apikey=736270cebb4e2191d31a70d74d7a9a782b6c747f087cb64eb01c2b62"
};

String getJson(const char* url);
void configureTime();
bool parseDate(const char* isoDate, struct tm* timeStruct);

//###################### SCREEN #####################################

// Screen dimensions
#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT 128 // Change this to 96 for 1.27" OLED.

// You can use any (4 or) 5 pins 
#define SCLK_PIN GPIO_NUM_18
#define MOSI_PIN GPIO_NUM_23 // attention pour celui la !!!! Il est à côté du GND
#define DC_PIN   GPIO_NUM_16
#define CS_PIN   GPIO_NUM_17
#define RST_PIN  GPIO_NUM_5

// Color definitions
#define	BLACK           0x0000
#define	BLUE            0x001F
#define	RED             0xF800
#define	GREEN           0x07E0
#define CYAN            0x07FF
#define MAGENTA         0xF81F
#define YELLOW          0xFFE0  
#define WHITE           0xFFFF
#define PINK            0xF81F 

#include <Adafruit_GFX.h>
#include <Adafruit_SSD1351.h>
#include <SPI.h>

// Option 1: use any pins but a little slower
//Adafruit_SSD1351 tft = Adafruit_SSD1351(SCREEN_WIDTH, SCREEN_HEIGHT, CS_PIN, DC_PIN, MOSI_PIN, SCLK_PIN, RST_PIN);  

// Option 2: must use the hardware SPI pins 
// (for UNO thats sclk = 13 and sid = 11) and pin 10 must be 
// an output. This is much faster - also required if you want
// to use the microSD card (see the image drawing example)
Adafruit_SSD1351 tft = Adafruit_SSD1351(SCREEN_WIDTH, SCREEN_HEIGHT, &SPI, CS_PIN, DC_PIN, RST_PIN);

//#######################################################################################################

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





  Serial.begin(115200);
  Serial.print("hello!");
  tft.begin();

  Serial.println("init");

  // You can optionally rotate the display by running the line below.
  // Note that a value of 0 means no rotation, 1 means 90 clockwise,
  // 2 means 180 degrees clockwise, and 3 means 270 degrees clockwise.
  //tft.setRotation(1);
  // NOTE: The test pattern at the start will NOT be rotated!  The code
  // for rendering the test pattern talks directly to the display and
  // ignores any rotation.



tft.fillScreen(BLACK);

}



void loop() {

int horaire[10];

int j = 0;

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
            //horaire[i] = minutes;
            horaire[j] = minutes;
            j = j+1;
            Serial.print(j);
            Serial.println(" j");
            
            // On a que i valeurs car on a deux temps pour le même i, donc quand il calcul le 2e temps, on est tjs sur le même i et donc il écrase la valeur dans le tableau "horaire".
            
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

for (auto i : horaire) {

  Serial.println("####################################################");
  Serial.println(i);
}

// Pour éviter que ça s'écrive par dessus.
tft.fillScreen(BLACK);

//14
tft.fillCircle(15,15,10, MAGENTA);
testdrawtext(10,11,1.5,14,BLACK);
testdrawtext(30,11,1.5,horaire[0],WHITE);
testdrawtext(60,11,1.5,horaire[1],WHITE);

//83
tft.fillCircle(15,45+1,10, GREEN);
testdrawtext(10,42,1.5,83,BLACK);
testdrawtext(30,42,1.5,horaire[2],WHITE);
testdrawtext(60,42,1.5,horaire[3],WHITE);

//13
tft.fillCircle(15,75+1,10, BLUE);
testdrawtext(10,72,1.5,13,BLACK);
testdrawtext(30,72,1.5,horaire[4],WHITE);
testdrawtext(60,72,1.5,horaire[5],WHITE);

//14
tft.fillCircle(15,105+1,10, MAGENTA);
testdrawtext(12,102,1.5,14,BLACK);
testdrawtext(32,102,1.5,horaire[6],WHITE);
testdrawtext(62,102,1.5,horaire[7],WHITE);

//9
tft.fillCircle(15,105+1,10, PINK);
testdrawtext(12,128,1.5,14,BLACK);
testdrawtext(32,128,1.5,horaire[8],WHITE);
testdrawtext(62,128,1.5,horaire[9],WHITE);



delay(50000);

}

void testdrawtext(int x, int y,int size, int text, uint16_t color) {
  
  tft.setCursor(x,y);
  tft.setTextColor(color);
  tft.setTextSize(size);
  tft.print(text);
}

// void testdrawtext(int x, int y,int size, char *text, uint16_t color) {
  
//   tft.setCursor(x,y);
//   tft.setTextColor(color);
//   tft.setTextSize(size);
//   tft.print(text);
// }

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
