from . import ItemKernel as it

#TODO: 리퀴드 하트

#칭호들


KingOfRootAbyss = it.Item(name="킹 오브 루타비스", att=3, stat_main = 8, stat_sub=8, potential = it.CharacterModifier(armor_ignore = 5, boss_pdamage = 5))
PingkbinAndMe = it.Item(name="핑아일체", att = 5, stat_main = 10, stat_sub=10, potential = it.CharacterModifier( boss_pdamage = 10))
MaplewellKnown = it.Item(name="메이플을 잘 아는", att = 5, stat_main = 10, stat_sub=10, potential = it.CharacterModifier( armor_ignore = 10))


# 칠요셋
WeeklyParkBadge = it.Item(name="칠요의 뱃지", stat_main = 7, stat_sub = 7, att = 7, armor_ignore = 19)  #뱃지가 따기 더 힘드므로 세트 옵션을 아예 임베딩
# 뱃지 방무와 세트 효과 방무는 별개이므로 방무 10퍼씩 2번 적용. (19퍼랑 동일)
WeeklyParkMedal = it.Item(name="칠요의 몬스터파커", stat_main = 7, stat_sub = 7, armor_ignore = 10)

def get_weekly_set():
    return {"badge" : WeeklyParkBadge.copy(),
                "medal" : WeeklyParkMedal.copy() }

def get_medal(value):
    return it.Item(name="훈장", att = value, stat_main = value, stat_sub = value)

def get_pet(att):   
    return it.Item(name="펫장비", att = att)

def get_heart(att, ptnl = it.CharacterModifier(), aptnl = it.CharacterModifier()):
    return it.Item(name="하트", att = att, potential = ptnl, additional_potential = aptnl)

def ocean_glow(star, each_enhance = it.CharacterModifier(), potential = it.CharacterModifier(),
                        additional_potential = it.CharacterModifier(),
                        bonus = it.CharacterModifier()):
    
    OceanGlowEaring = it.Item(name="오션 글로우 이어링", stat_main = 7, stat_sub = 5, att = 5)
    OceanGlowEaring.add_main_option(bonus)
    OceanGlowEaring.set_potential(potential)
    OceanGlowEaring.set_additional_potential(additional_potential)
    
    scroll_enhance = it.CharacterModifier()
    for i in range(8):
        scroll_enhance += each_enhance
    OceanGlowEaring.add_main_option(scroll_enhance)
    OceanGlowEaring.add_main_option(it.EnhancerFactory.get_armor_starforce_enhancement(150, star))
    return OceanGlowEaring

