from esphome.components import select
import esphome.config_validation as cv
import esphome.codegen as cg
from esphome.const import (
    CONF_ID,
    CONF_TYPE,
    CONF_ICON,
    CONF_OPTIONS,
    ICON_THERMOMETER,
    CONF_ENTITY_CATEGORY,
    CONF_DISABLED_BY_DEFAULT,
)
from .. import truma_inetbox_ns, CONF_TRUMA_INETBOX_ID, TrumaINetBoxApp

DEPENDENCIES = ["truma_inetbox"]
CODEOWNERS = ["@Fabian-Schmidt"]

CONF_CLASS = "class"

TrumaSelect = truma_inetbox_ns.class_(
    "TrumaSelect", select.Select, cg.Component)

# `TRUMA_SELECT_TYPE` is a enum class and not a namespace but it works.
TRUMA_SELECT_TYPE_dummy_ns = truma_inetbox_ns.namespace("TRUMA_SELECT_TYPE")

CONF_SUPPORTED_TYPE = {
    "HEATER_FAN_MODE_COMBI": {
        CONF_CLASS: truma_inetbox_ns.class_("TrumaHeaterSelect", select.Select, cg.Component),
        CONF_TYPE: TRUMA_SELECT_TYPE_dummy_ns.HEATER_FAN_MODE,
        CONF_ICON: ICON_THERMOMETER,
        CONF_OPTIONS: ("Off", "Eco", "High", "Boost"),
    },
    "HEATER_FAN_MODE_VARIO_HEAT": {
        CONF_CLASS: truma_inetbox_ns.class_("TrumaHeaterSelect", select.Select, cg.Component),
        CONF_TYPE: TRUMA_SELECT_TYPE_dummy_ns.HEATER_FAN_MODE,
        CONF_ICON: ICON_THERMOMETER,
        CONF_OPTIONS: ("Off", "Night", "Auto", "Boost"),
    },
    "HEATER_ENERGY_MIX_GAS": {
        CONF_CLASS: truma_inetbox_ns.class_("TrumaHeaterSelect", select.Select, cg.Component),
        CONF_TYPE: TRUMA_SELECT_TYPE_dummy_ns.HEATER_ENERGY_MIX,
        CONF_ICON: ICON_THERMOMETER,
        CONF_OPTIONS: ("Gas", "Mix 1", "Mix 2", "Electric 1", "Electric 2"),
    },
    "HEATER_ENERGY_MIX_DIESEL": {
        CONF_CLASS: truma_inetbox_ns.class_("TrumaHeaterSelect", select.Select, cg.Component),
        CONF_TYPE: TRUMA_SELECT_TYPE_dummy_ns.HEATER_ENERGY_MIX,
        CONF_ICON: ICON_THERMOMETER,
        CONF_OPTIONS: ("Diesel", "Mix 1", "Mix 2", "Electric 1", "Electric 2"),
    },
}


def set_default_based_on_type():
    def set_defaults_(config):
        type_key = config[CONF_TYPE].upper()  
        type_data = CONF_SUPPORTED_TYPE[type_key]
        config[CONF_ID].type = type_data[CONF_CLASS]
        if CONF_ICON not in config:
            config[CONF_ICON] = type_data[CONF_ICON]
        if CONF_OPTIONS not in config:
            config[CONF_OPTIONS] = type_data[CONF_OPTIONS]
        return config

    return set_defaults_


SELECT_SCHEMA_BASE = select.select_schema({})
CONFIG_SCHEMA = cv.Schema({
    **SELECT_SCHEMA_BASE.schema,
    cv.GenerateID(): cv.declare_id(TrumaSelect),
    cv.GenerateID(CONF_TRUMA_INETBOX_ID): cv.use_id(TrumaINetBoxApp),
    cv.Required(CONF_TYPE): cv.one_of(*CONF_SUPPORTED_TYPE.keys()),
    cv.Optional(CONF_ICON): cv.icon,
    cv.Optional(CONF_OPTIONS): cv.All(
        cv.ensure_list(cv.string_strict), cv.Length(min=1)
    ),
    cv.Optional(CONF_ENTITY_CATEGORY): cv.entity_category,
    cv.Optional(CONF_DISABLED_BY_DEFAULT, default=False): cv.boolean,
}).extend(cv.COMPONENT_SCHEMA)
FINAL_VALIDATE_SCHEMA = set_default_based_on_type()


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await select.register_select(
        var,
        config,
        options=config[CONF_OPTIONS]
    )
    await cg.register_parented(var, config[CONF_TRUMA_INETBOX_ID])

    type_key = config[CONF_TYPE].upper()
    cg.add(var.set_type(CONF_SUPPORTED_TYPE[type_key][CONF_TYPE]))
