# shipBonusRemoteArmorRepairAmountGF2
#
# Used by:
# Ship: Navitas
type = "passive"
def handler(fit, ship, context):
    fit.modules.filteredItemBoost(lambda mod: mod.item.group.name == "Remote Armor Repairer",
                                  "armorDamageAmount", ship.getModifiedItemAttr("shipBonusGF2"), skill="Gallente Frigate")
