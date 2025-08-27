from esphome.components import climate
import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.const import (
    CONF_ID,
    CONF_TYPE,
    CONF_VISUAL,
    CONF_TARGET_TEMPERATURE,
    CONF_MIN_TEMPERATURE,
    CONF_MAX_TEMPERATURE,
    CONF_TEMPERATURE_STEP,
)
from esphome.components.climate import (
    ClimateMode,
)

CLIMATE_MODES = {
    "OFF": ClimateMode.CLIMATE_MODE_OFF,
    "HEAT": ClimateMode.CLIMATE_MODE_HEAT,
    "AUTO": ClimateMode.CLIMATE_MODE_AUTO,
}
CLIMATE_VISUAL_SCHEMA = cv.Schema({
    cv.Optional(CONF_TARGET_TEMPERATURE, default={}): cv.Schema({
        cv.Optional(CONF_MIN_TEMPERATURE, default=5.0): cv.float_,
        cv.Optional(CONF_MAX_TEMPERATURE, default=30.0): cv.float_,
        cv.Optional(CONF_TEMPERATURE_STEP, default=0.5): cv.float_,
    })
})
from .. import truma_inetbox_ns, CONF_TRUMA_INETBOX_ID, TrumaINetBoxApp

DEPENDENCIES = ["truma_inetbox"]
CODEOWNERS = ["@Fabian-Schmidt"]

TrumaClimate = truma_inetbox_ns.class_(
    "TrumaClimate", climate.Climate, cg.Component)

CONF_SUPPORTED_TYPE = {
    "ROOM": truma_inetbox_ns.class_("TrumaRoomClimate", climate.Climate, cg.Component),
    "WATER": truma_inetbox_ns.class_("TrumaWaterClimate", climate.Climate, cg.Component),
}


def set_default_based_on_type():
    def set_defaults_(config):
        # update the class
        config[CONF_ID].type = CONF_SUPPORTED_TYPE[config[CONF_TYPE]]
        return config

    return set_defaults_


CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(TrumaClimate),
    cv.GenerateID(CONF_TRUMA_INETBOX_ID): cv.use_id(TrumaINetBoxApp),
    cv.Required(CONF_TYPE): cv.enum(CONF_SUPPORTED_TYPE, upper=True),

    cv.Optional(CONF_NAME, default="Truma Climate"): cv.string,

    cv.Optional("preset"): cv.All(cv.ensure_list(cv.string)),  # If you want presets
    cv.Optional("supported_modes", default=["OFF", "HEAT"]): cv.ensure_list(cv.enum(CLIMATE_MODES, upper=True)),
}).extend(cv.COMPONENT_SCHEMA).extend({
    cv.Optional("disabled_by_default", default=False): cv.boolean,
    cv.Optional("entity_category"): cv.entity_category,
    cv.Optional("icon"): cv.icon,
    cv.Optional(CONF_VISUAL, default={}): CLIMATE_VISUAL_SCHEMA,
})
FINAL_VALIDATE_SCHEMA = set_default_based_on_type()


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)
    await cg.register_parented(var, config[CONF_TRUMA_INETBOX_ID])
    if "supported_modes" in config:
        modes = [CLIMATE_MODES[m] for m in config["supported_modes"]]        
        modes = [CLIMATE_MODES[m] for m in config["supported_modes"]]
        cg.add(var.set_supported_modes(modes))        
        cg.add(var.set_supported_modes(modes))