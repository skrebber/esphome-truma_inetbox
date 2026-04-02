#ifdef USE_ESP32_FRAMEWORK_ESP_IDF

#include "LinBusListener.h"
#include "esphome/core/log.h"

//#ifdef CUSTOM_ESPHOME_UART
//#include "esphome/components/uart/truma_uart_component_esp_idf.h"
//#define ESPHOME_UART uart::truma_IDFUARTComponent
//#else
#include "esphome/components/uart/uart_component_esp_idf.h"
#define ESPHOME_UART uart::IDFUARTComponent
//#endif  // CUSTOM_ESPHOME_UART

#include <driver/uart.h>

namespace esphome {
namespace truma_inetbox {

static const char *const TAG = "truma_inetbox.LinBusListener";

void LinBusListener::setup_framework() {
  auto *uart_comp = static_cast<ESPHOME_UART *>(this->parent_);
  uart_port_t uart_num = static_cast<uart_port_t>(uart_comp->get_hw_serial_number());

  // Keep receive latency low so ESPHome's loop wakeup sees bytes immediately.
  // We no longer create our own UART event task or consume an event queue.
  esp_err_t err = uart_set_rx_full_threshold(uart_num, 1);
  if (err != ESP_OK) {
    ESP_LOGW(TAG, "uart_set_rx_full_threshold failed: %s", esp_err_to_name(err));
  }

  err = uart_set_rx_timeout(uart_num, 2);
  if (err != ESP_OK) {
    ESP_LOGW(TAG, "uart_set_rx_timeout failed: %s", esp_err_to_name(err));
  }

  ESP_LOGCONFIG(TAG, "UART configured for loop-driven RX processing");
}

}  // namespace truma_inetbox
}  // namespace esphome

#undef ESPHOME_UART

#endif  // USE_ESP32_FRAMEWORK_ESP_IDF