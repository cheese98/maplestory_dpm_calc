from . import ItemKernel as it
ExMDF = it.ExMDF

#TODO : 이런 프로세스들을 좀 더 factorization 할 수는 없을까..

EventRing = it.Item(name="이벤트 링", level = 120, main_option = ExMDF(stat_main = 30, stat_sub = 30, att = 20))
def getEventRing(potential = it.ExMDF(), additional_potential = it.ExMDF()):
    item = EventRing.copy()
    item.set_potential(potential)
    item.set_additional_potential(additional_potential)
    return item

Subweapon = it.Item(name="보조무기", level = 100, main_option = ExMDF(stat_main = 10, stat_sub = 10, att = 3))
def getSubweapon(potential = it.ExMDF(), additional_potential = it.ExMDF()):
    item = Subweapon.copy()
    item.set_potential(potential)
    item.set_additional_potential(additional_potential)
    return item
    
Emblem = it.Item(name="엠블럼", level = 100, main_option = ExMDF(stat_main = 10, stat_sub = 10, att = 2))
def getEmblem(potential = it.ExMDF(), additional_potential = it.ExMDF()):
    item = Emblem.copy()
    item.set_potential(potential)
    item.set_additional_potential(additional_potential)
    return item

def get_subweapon_covering_exception(_type, star, elist, potential = it.ExMDF(), additional_potential = it.ExMDF(), factory_hook=None):
    if _type == '블레이드':
        return factory_hook.getBlade(_type, star=star, elist=elist, potential = potential, additional_potential = additional_potential)
    elif _type == '제로무기':
        return factory_hook.getZeroSubweapon(_type, potential = potential, additional_potential = additional_potential)
    else:
        return getSubweapon(potential=potential, additional_potential=additional_potential)