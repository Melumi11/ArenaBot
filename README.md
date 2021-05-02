<div align="center">
<h1>ArenaBot: a multiplayer roleplay fighting discord bot</h1>
</div>

![](https://github.com/Melumi11/ArenaBot/blob/main/demo.png)

### Index

-   [ArenaBot](#)
    -   [Features](#features)
    -   [Notes](#notes)
    -   [Fight Rules](#fight-rules)
         - [Base Rules](#base-rules)
         - [Number Rules](#number-rules)
         - [Comeback Rules](#comeback-rules)
         - [Clash Rules](#clash-rules)
         - [Draw Rules](#draw-rules)
         - [Stat Notes](#stat-notes)
         - [Invalidation Notes](#invalidation-notes)
         - [Other Notes](#other-notes)
         - [Battle Awards](#battle-awards)
         - [Stats Template](#stats-template)

### Features:

-   **Slash Commands** - They're super cool and fancy
-   **Epic Commands** - Like /fight and /roll
-   **Parm** - ████████
-   **Suports Concurrent Fights** - Multiple fights between different fighters can be fought at the same time

### Notes:
This bot was created for a discord server that I am a part of called "The ARENA" where I and some friends do roleplay fights.

These fight rules were written by StealthMsopz and the folks from The ARENA.

ArenaBot Support Server: https://discord.gg/fwUpkpCY5U

# Fight Rules:
### Base Rules:
- Players start with 100 HP. (You can be at more than 100 HP.)
- Each round both players roll a 20 sided die. (!roll d20)
- The number rolled is the damage dealt.
- The first player to lose all their HP loses.

### Number Rules:
- 1 rolls are missed attacks and do no damage.
- 17 rolls can either do 17 damage or heal using four 7 sided dice. (!roll 4d7 and heal between 7 and 28 HP.)
- Rolling a number 3 times in a row gives the player an extra roll. (Does not apply to !roll 4d7 or !roll d100. Counter is reset after the third roll.)
- Rolling three 1s in a row gives the player an extra 40 sided die roll. (!roll d40)
- If a player rolls their own lucky number they heal 10 HP. (Does not apply to !roll 4d7 or !roll d100.)

### Comeback Rules:
- If the difference between the players' HP is 30 or greater, then the player with lower HP can roll a 30 sided die. (!roll d30)
- The HP difference required is lowered to 25 HP if the player is at 5 HP or less. (Player 1 HP: 5- & Player 2 HP: 30+) 

### Clash Rules:
- If both players roll the same number then a clash is started. (1 rolls cannot start clashes due to both players missing.)
- Both players roll a 100 sided die and whoever gets the higher number twice wins. (!roll d100 best 2 out of 3.)
- If you roll the same number during a clash, then redo the roll.
- Rolling a 100 wins the clash instantly, while rolling a 1 loses the clash instantly.
- The winner will use the roll that the clash was started with, while the loser does nothing.

### Draw Rules:
- If both players hit 0 HP or lower, it results in a draw.
- A draw will give both players a draw stat, not a win or loss stat.
- A draw clash is started, in which the winner may get an award and add a clash win to their stats. (Best 3 out of 5.)

### Stat Notes:
- Numbers rolled using !roll 4d7 or !roll d100 do not count towards stats.
- 17 Heals Used stat is only affected if the player chooses to use the 17 roll as a heal.
- The 30 rolls stat is only for if you roll a 30 exactly, not if you roll a 30 sided die.
- Clash Wins stat is only affected if you win the clash.

### Invalidation Notes:
- If there is an invalid roll (such as using !roll d30 against the rules) then redo the roll correctly.
- Calculating the HP incorrectly or forgetting to heal 10 HP from a lucky number is considered a mistake and can be corrected later on.
- If you are far in the game and a mistake is noticed early on, you can either rewind, restart, or continue playing based on how game changing the mistake was. (For example, if the mistake put them at a 30 HP gap, then a d30 came into play. This can change the results of the battle.)
- Situations like forgetting that 17s can be used for healing are considered as mistakes and not invalidations.
- In some cases, battles and stats earned from said battles will be invalidated. Also, remember that both players roll at the same time, so there is no need for both players to reroll if only one made a mistake.
- Please do not delete rolls illegally and make sure to get both player's permission before making deleting, rewinding, restarting, etc.

### Other Notes:
- Do not forfeit. If you forfeit the battle will be invalidated and you will wear the hat of shame.
- Don’t be afraid to ask questions. If you qualify for an award, feel free to write it down.
- Tip: Before deciding to heal or damage using a 17 roll, see what the opponent rolls first. Both players roll at the same time, so making a decision before your opponent moves can put you at a disadvantage.
- Specials are currently 20s (or 30s), but as of now are only for show. Unique attributes or other aspects for specials may be added in the future.
- Draw clashes are optional but they have benefits for official battles. (Awards and stats!)
- Awards will only be given for official fights. (Includes story fights.)
- If a player is able to use a d30 or a d40, they may still decide to use a d20.
- Clashes started with lucky numbers or 20s count towards stats for both players. This includes 1s, even though 1s cannot start clashes. For 17s, however, you must win the clash to use a 17 heal and have it count towards stats.

### Battle Awards: 
(Feel free to suggest awards and keep your eyes open in case you qualify for one.)

**1 HP** - Win a fight at 1 HP.

**Exact Elimination** - Finish an opponent with the exact number.

**Opening Gambit** - Roll a 20 while the opponent rolls a 1 on the first turn.

**Opening Clasher** - Win a clash on the first turn of a fight.

**Draw Clasher I** - Win a draw clash.

**Draw Clasher II** - Win 3 draw clashes.

**Draw Clasher III** - Win 5 draw clashes.

**Draw Clasher IV** - Win 10 draw clashes.

**Overkill** - Win and get an opponent to -15 HP or lower.

**Special Finisher** - Finish an opponent with a 20 roll.

**Clash Finisher** - Finish an opponent with a clash. (Does not apply to Draw Clashes.)

**Lucky Finisher** - Finish an opponent with your lucky number.

**Unwavering** - Win after a comeback rule was activated earlier in the fight. 

**Determination** - Win after the opponent had 50 HP or more than you earlier in the fight.

**Threefold** - Roll a number three times in a row.

**Fourfold** - Roll a number four times in a row.

**Fivefold** - Roll a number five times in a row.

**Karma** - Roll three 1s in a row.

**Berserker** - Roll three 20s in a row.

**Frenzy** - Win 3 times in a row.

**Slaughter** - Win 5 times in a row.

**Massacre** - Win 10 times in a row.

**Untouchable** - Win a fight at 30 HP or more.

**Invincible** - Win a fight at 50 HP or more.

**Immortal** - Win a fight at 70 HP or more.

**Life Saver** - Reach 125 HP or more.

**Unyielding** - Heal yourself using a 17 roll or a lucky number in the face of death.

**Undying** - Win after healing yourself using a 17 roll or a lucky number in the face of death.

**Clash 100** - Roll a 100 during a clash for an instant clash win.

**Punisher** - Roll a 30 using a d30.



### Stats Template:

Stats: (Name)

Special:

Weapon:

Lucky Number: (Can't be 1, 17, 20 or another player's number.)



Total Games:

Wins:

Losses:

Draws:



1s Rolled:

20s Rolled:

Lucky Numbers Rolled:

17 Heals Used:

Clash Wins:
