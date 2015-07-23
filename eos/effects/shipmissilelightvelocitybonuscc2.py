# shipMissileLightVelocityBonusCC2
#
# Used by:
# Ship: Caracal
# Ship: Osprey Navy Issue
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Light Missiles"),
                                    "maxVelocity", ship.getModifiedItemAttr("shipBonusCC2"), skill="Caldari Cruiser")
