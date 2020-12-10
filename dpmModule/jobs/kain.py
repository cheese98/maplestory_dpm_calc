from functools import partial
from ..kernel import core
from ..character import characterKernel as ck
from ..status.ability import Ability_tool
from ..execution.rules import RuleSet
from . import globalSkill
from .jobbranch import bowmen
from math import ceil
from typing import Any, Dict


class JobGenerator(ck.JobGenerator):
    def __init__(self):
        super(JobGenerator, self).__init__()
        self.vEnhanceNum = 10
        self.jobtype = "dex"
        self.jobname = "카인"
        self.ability_list = Ability_tool.get_ability_set(
            "boss_pdamage", "crit", "buff_rem"
        )
        self.preEmptiveSkills = 1

    def get_modifier_optimization_hint(self):
        return core.CharacterModifier()

    def get_ruleset(self):
        ruleset = RuleSet()
        return ruleset

    def get_passive_skill_list(
        self, vEhc, chtr: ck.AbstractCharacter, options: Dict[str, Any]
    ):
        passive_level = chtr.get_base_modifier().passive_level + self.combat
        Hitman = core.InformedCharacterModifier("히트맨", att=40, crit=35)
        BreathShooterMastery = core.InformedCharacterModifier("브레스 슈터 마스터리", att=30)
        PhysicalTraining = core.InformedCharacterModifier("피지컬 트레이닝", stat_main=60)
        NaturalBornInstinct = core.InformedCharacterModifier(
            "네츄럴 본 인스팅트", pdamage_indep=25, att=40, crit=20, armor_ignore=10
        )
        GrindingII = core.InformedCharacterModifier("그라인딩 II", att=30 + passive_level)
        Dogma = core.InformedCharacterModifier(
            "도그마",
            pdamage_indep=20 + passive_level // 2,
            crit_damage=20 + passive_level,
            armor_ignore=30 + passive_level,
        )
        BreathShooterExpert = core.InformedCharacterModifier(
            "브레스 슈터 엑스퍼트",
            pdamage_indep=30 + passive_level // 2,
            att=30 + passive_level,
            crit_damage=20 + passive_level // 2,
        )
        AdaptToDeath = core.InformedCharacterModifier(
            "어댑트 투 데스",
            pdamage=10 + ceil(passive_level / 2),
            boss_pdamage=10 + passive_level // 4,
        )

        return [
            Hitman,
            BreathShooterMastery,
            PhysicalTraining,
            NaturalBornInstinct,
            GrindingII,
            Dogma,
            BreathShooterExpert,
            AdaptToDeath,
        ]

    def get_not_implied_skill_list(
        self, vEhc, chtr: ck.AbstractCharacter, options: Dict[str, Any]
    ):
        passive_level = chtr.get_base_modifier().passive_level + self.combat
        WeaponConstant = core.InformedCharacterModifier("무기상수", pdamage_indep=35)
        Mastery = core.InformedCharacterModifier(
            "숙련도", pdamage_indep=-7.5 + 0.5 * ceil(passive_level / 2)
        )

        return [WeaponConstant, Mastery]

    def generate(self, vEhc, chtr: ck.AbstractCharacter, options: Dict[str, Any]):
        """"""
        passive_level = chtr.get_base_modifier().passive_level + self.combat

        # Damage Skills
        StrikeArrowI = core.DamageSkill(
            name="스트라이크 애로우",
            delay=450,  # base delay 570
            damage=70 + 89 + 79 + 85 + passive_level,
            hit=5,
        ).wrap(core.DamageSkillWrapper)
        StrikeArrowII = core.DamageSkill(
            name="스트라이크 애로우 II",
            delay=450,  # base delay 570
            damage=160 + 79 + 85 + passive_level,
            hit=5,
        ).wrap(core.DamageSkillWrapper)
        StrikeArrowRelease = core.DamageSkill(
            name="스트라이크 애로우 발현",
            delay=450,  # base delay 570
            damage=200 + 80 + 85 + passive_level,
            hit=8,
            cooltime=1000,
        ).wrap(core.DamageSkillWrapper)
        StrikeArrowIII = core.DamageSkill(
            name="스트라이크 애로우 III",
            delay=450,  # base delay 570
            damage=240 + 85 + passive_level,
            hit=5,
        ).wrap(core.DamageSkillWrapper)

        ScatteringShot = core.StackableDamageSkillWrapper(
            core.DamageSkill(
                name="스캐터링 샷",
                delay=480,  # base delay 630
                damage=120 + 75 + 75 + passive_level,
                hit=4,
                cooltime=6000,
            ),
            3,
        )
        ScatteringShotExceed = core.DamageSkill(
            name="스캐터링 샷(초과)",
            delay=0,
            damage=120 + 75 + 75 + passive_level,
            hit=4,  # 4회 반복
            cooltime=-1,
            modifier=core.CharacterModifier(pdamage_indep=-50),
        ).wrap(core.DamageSkillWrapper)
        ScatteringShotRelease = core.DamageSkill(
            name="스캐터링 샷 발현",
            delay=480,  # base delay 630
            damage=135 + 80 + 80 + passive_level,
            hit=4,
            cooltime=7000,
        ).wrap(core.DamageSkillWrapper)
        ScatteringShotReleaseExceed = core.DamageSkill(
            name="스캐터링 샷 발현(초과)",
            delay=0,
            damage=135 + 80 + 80 + passive_level,
            hit=4,  # 5회 반복
            modifier=core.CharacterModifier(pdamage_indep=-50),
        ).wrap(core.DamageSkillWrapper)

        Posession = core.BuffSkill(
            name="포제션",
            delay=0,  # base delay 270, 다른 스킬 딜레이 중 사용 가능 -> 0
            remain=15000,
            cooltime=30,
        ).wrap(core.BuffSkillWrapper)
        Malice = core.StackSkillWrapper(
            core.BuffSkill(name="멜리스", delay=0, remain=9999999), 499
        )
        MaliceTick = core.SummonSkill(
            name="멜리스(자연회복)",
            summondelay=0,
            delay=1020,
            damage=0,
            hit=0,
            remain=99999999,
        ).wrap(core.SummonSkillWrapper)

        # V skills
        CriticalReinforce = bowmen.CriticalReinforceWrapper(vEhc, chtr, 0, 0, 10)

        ######   Skill Wrapper   ######
        # Malice
        MaliceTick.onAfter(Malice.stackController(10))
        AddMalice = Malice.stackController(17)
        for sk in [
            StrikeArrowI,
            StrikeArrowII,
            StrikeArrowIII,
            StrikeArrowRelease,
            ScatteringShot,
            ScatteringShotExceed,
            ScatteringShotRelease,
            ScatteringShotReleaseExceed,
        ]:
            sk.onJustAfter(AddMalice)

        # Posession
        Posession.onConstraint(
            core.ConstraintElement("멜리스 스톤 > 1", Malice, partial(Malice.judge, 100, 1))
        )
        Posession.onJustAfter(Malice.stackController(-100))

        # Scattering Shot
        ScatteringShot.onJustAfter(core.RepeatElement(ScatteringShotExceed, 4))
        ScatteringShotRelease.onJustAfter(
            core.RepeatElement(ScatteringShotReleaseExceed, 5)
        )

        # Release
        IsPosession = core.ConstraintElement("포제션 ON", Posession, Posession.is_active)
        NotPosession = core.ConstraintElement(
            "포제션 OFF", Posession, Posession.is_not_active
        )
        for sk in [StrikeArrowRelease, ScatteringShotRelease]:
            sk.onConstraint(IsPosession)
            sk.onJustAfter(Posession.controller(1))
        for sk in [ScatteringShot]:
            sk.onConstraint(NotPosession)

        # TODO: 정확히는 StrikeArrowRelease를 BasicAttack에 끼워넣어야 하지만...
        StrikeArrowI.onAfter(StrikeArrowII)
        StrikeArrowII.onAfter(StrikeArrowIII)

        return (
            StrikeArrowI,
            [
                Malice,
                globalSkill.maple_heros(
                    chtr.level, name="노바의 용사", combat_level=self.combat
                ),
                globalSkill.useful_sharp_eyes(),
                globalSkill.useful_combat_orders(),
                globalSkill.soul_contract(),
                CriticalReinforce,
            ]
            + [MaliceTick]
            + [ScatteringShot, ScatteringShotExceed]
            + [StrikeArrowI],
        )
