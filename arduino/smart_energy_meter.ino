/**
 * Smart Energy Meter - Firmware Arduino
 *
 * Mede tensão, corrente e potência da rede elétrica usando:
 * - Sensor de corrente SCT013
 * - Transformador de tensão (ZMPT101B ou similar)
 * - Display LCD I2C 16x2
 *
 * Envia os dados via serial no formato:
 *   potencia|tensao|corrente|valor|tempo
 *
 * Bibliotecas necessárias:
 *   - EmonLib (OpenEnergyMonitor)
 *   - LiquidCrystal_I2C
 *   - Wire
 */

#include <LiquidCrystal_I2C.h>
#include <EmonLib.h>
#include <Wire.h>

// === CONFIGURAÇÕES ===
#define VOLT_CAL 520       // Calibração de tensão (ajustar com multímetro)
#define CURRENT_CAL 6.0606 // Calibração de corrente (SCT013-030: 30A/1V)
#define SERIAL_BAUD 9600
#define LCD_ADDRESS 0x27
#define LCD_COLS 16
#define LCD_ROWS 2
#define TARIFA_KWH 0.92    // Tarifa em R$/kWh (ajustar conforme sua região)

// === VARIÁVEIS GLOBAIS ===
float potencia = 0;
float valor_acumulado = 0;
double tempo_s = 0;

// === INSTÂNCIAS ===
EnergyMonitor sensor_corrente;
EnergyMonitor sensor_tensao;
LiquidCrystal_I2C lcd(LCD_ADDRESS, LCD_COLS, LCD_ROWS);

void setup() {
    Serial.begin(SERIAL_BAUD);

    // Configuração dos sensores
    sensor_tensao.voltage(0, VOLT_CAL, 1.7);
    sensor_corrente.current(1, CURRENT_CAL);

    // Configuração do LCD
    lcd.init();
    lcd.setBacklight(HIGH);
    lcd.setCursor(0, 0);
    lcd.print("Smart Energy");
    lcd.setCursor(0, 1);
    lcd.print("Meter v1.0");
    delay(2000);
    lcd.clear();
}

void loop() {
    // Leitura dos sensores
    double corrente = sensor_corrente.calcIrms(1480);
    sensor_tensao.calcVI(17, 2000);
    float tensao = sensor_tensao.Vrms;

    // Cálculos
    potencia = corrente * tensao;
    float tarifa_por_segundo = TARIFA_KWH / 3600.0;
    valor_acumulado += (potencia / 1000.0) * tarifa_por_segundo;
    tempo_s = millis() / 1000.0;

    // Display LCD - Página 1
    lcd.setCursor(0, 0);
    lcd.print("POT:");
    lcd.print(potencia, 1);
    lcd.print("W   ");
    lcd.setCursor(0, 1);
    lcd.print("V:");
    lcd.print(tensao, 1);
    lcd.print("V   ");
    delay(1000);

    // Display LCD - Página 2
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("I:");
    lcd.print(corrente, 3);
    lcd.print("A   ");
    lcd.setCursor(0, 1);
    lcd.print("R$:");
    lcd.print(valor_acumulado, 4);
    delay(1000);
    lcd.clear();

    // Envio via serial (formato: potencia|tensao|corrente|valor|tempo)
    Serial.println(
        String(potencia) + "|" +
        String(tensao) + "|" +
        String(corrente) + "|" +
        String(valor_acumulado) + "|" +
        String(tempo_s)
    );
}
