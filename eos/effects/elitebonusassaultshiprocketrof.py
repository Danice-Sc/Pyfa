# eliteBonusAssaultShipRocketROF
#
# Used by:
# Ship: Cambion
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Missile Launcher Rocket",
                                  "speed", ship.getModifiedItemAttr("eliteBonusGunship1"), skill="Assault Frigates")
