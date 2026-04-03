"""
Battle Engine for Pokémon Battle Arena
Handles battle mechanics, damage calculation, and turn resolution
"""
import random
from typing import Dict, List, Tuple, Optional
from task3.database import get_type_effectiveness


class Pokemon:
    """Battle Pokemon instance with current state"""
    
    def __init__(self, data: Dict, player: str):
        if not data:
            raise ValueError("Pokemon data cannot be None")

        self.id = data.get('id')
        self.name = data['name']
        self.type_1 = data.get('type_1', data.get('type1'))
        self.type_2 = data.get('type_2', data.get('type2'))
        self.max_hp = data['hp']
        self.current_hp = data['hp']
        self.attack = data['attack']
        self.defense = data['defense']
        self.sp_atk = data.get('sp_atk')
        self.sp_def = data.get('sp_def')
        self.speed = data['speed']
        self.player = player
        self.is_fainted = False
    
    def take_damage(self, damage: int):
        """Apply damage to Pokémon"""
        self.current_hp = max(0, self.current_hp - damage)
        if self.current_hp == 0:
            self.is_fainted = True
    
    def is_alive(self) -> bool:
        """Check if Pokémon can still battle"""
        return not self.is_fainted and self.current_hp > 0
    
    def get_hp_percentage(self) -> float:
        """Get HP as percentage"""
        return (self.current_hp / self.max_hp) * 100 if self.max_hp > 0 else 0
    
    def __str__(self):
        return f"{self.name} ({self.current_hp}/{self.max_hp} HP)"


class BattleEngine:
    """Manages battle state and mechanics"""
    
    def __init__(self, team1: List[Dict], team2: List[Dict]):
        valid_team1 = [p for p in team1 if p]
        valid_team2 = [p for p in team2 if p]

        if not valid_team1 or not valid_team2:
            raise ValueError("Both teams must contain at least one valid Pokemon")

        self.team1 = [Pokemon(p, "Player 1") for p in valid_team1]
        self.team2 = [Pokemon(p, "Player 2") for p in valid_team2]
        
        self.current_p1 = 0  # Index of current active Pokémon
        self.current_p2 = 0
        
        self.battle_log = []
        self.turn_number = 0
        self.winner = None
    
    def get_active_pokemon(self) -> Tuple[Optional[Pokemon], Optional[Pokemon]]:
        """Get currently active Pokémon for both players"""
        p1 = self.team1[self.current_p1] if self.current_p1 < len(self.team1) else None
        p2 = self.team2[self.current_p2] if self.current_p2 < len(self.team2) else None
        return p1, p2
    
    def calculate_damage(self, attacker: Pokemon, defender: Pokemon, move_type: str = None) -> Tuple[int, float, str]:
        """
        Calculate damage based on Pokémon stats and type effectiveness
        
        Formula: Damage = ((2 * Level / 5 + 2) * Power * A/D / 50 + 2) * Modifier
        Simplified for this implementation:
        Damage = (Attack * Power / Defense) * Type_Effectiveness * Random(0.85, 1.0)
        """
        
        # Use attacker's primary type if no move type specified
        if move_type is None:
            move_type = attacker.type_1
        
        # Base power (simplified - using attack stat as power)
        base_power = 50
        
        # Calculate base damage
        attack_stat = attacker.attack
        defense_stat = defender.defense
        
        base_damage = ((attack_stat * base_power) / defense_stat) * 0.4
        
        # Type effectiveness
        effectiveness = get_type_effectiveness(move_type, defender.type_1, defender.type_2)
        
        # Determine effectiveness message
        if effectiveness == 0:
            eff_msg = "It has no effect!"
        elif effectiveness < 1:
            eff_msg = "It's not very effective..."
        elif effectiveness > 1:
            eff_msg = "It's super effective!"
        else:
            eff_msg = ""
        
        # Random factor (0.85 to 1.0)
        random_factor = random.uniform(0.85, 1.0)
        
        # Calculate final damage
        final_damage = int(base_damage * effectiveness * random_factor)
        
        # Minimum damage of 1 (unless immune)
        if effectiveness > 0:
            final_damage = max(1, final_damage)
        
        return final_damage, effectiveness, eff_msg
    
    def execute_turn(self) -> List[str]:
        """Execute one turn of battle"""
        self.turn_number += 1
        turn_log = [f"\n━━━ Turn {self.turn_number} ━━━"]
        
        p1, p2 = self.get_active_pokemon()
        
        if not p1 or not p2:
            return turn_log
        
        # Determine turn order based on Speed
        if p1.speed >= p2.speed:
            first, second = p1, p2
        else:
            first, second = p2, p1
        
        # First Pokémon attacks
        if first.is_alive() and second.is_alive():
            damage, effectiveness, eff_msg = self.calculate_damage(first, second)
            second.take_damage(damage)
            
            turn_log.append(f"⚔️ {first.name} attacks {second.name}!")
            turn_log.append(f"   💥 {damage} damage dealt! {eff_msg}")
            turn_log.append(f"   {second.name}: {second.current_hp}/{second.max_hp} HP")
            
            if second.is_fainted:
                turn_log.append(f"   💀 {second.name} fainted!")
                if not self.switch_pokemon(second.player):
                    self.winner = first.player
                    turn_log.append(f"\n🏆 {self.winner} wins the battle!")
                    return turn_log
        
        # Second Pokémon attacks (if still alive)
        if second.is_alive() and first.is_alive():
            damage, effectiveness, eff_msg = self.calculate_damage(second, first)
            first.take_damage(damage)
            
            turn_log.append(f"⚔️ {second.name} attacks {first.name}!")
            turn_log.append(f"   💥 {damage} damage dealt! {eff_msg}")
            turn_log.append(f"   {first.name}: {first.current_hp}/{first.max_hp} HP")
            
            if first.is_fainted:
                turn_log.append(f"   💀 {first.name} fainted!")
                if not self.switch_pokemon(first.player):
                    self.winner = second.player
                    turn_log.append(f"\n🏆 {self.winner} wins the battle!")
                    return turn_log
        
        self.battle_log.extend(turn_log)
        return turn_log
    
    def switch_pokemon(self, player: str) -> bool:
        """
        Switch to next available Pokémon
        Returns True if switch successful, False if no Pokémon left
        """
        if player == "Player 1":
            self.current_p1 += 1
            if self.current_p1 < len(self.team1):
                next_pokemon = self.team1[self.current_p1]
                self.battle_log.append(f"   🔄 Player 1 sends out {next_pokemon.name}!")
                return True
            return False
        else:
            self.current_p2 += 1
            if self.current_p2 < len(self.team2):
                next_pokemon = self.team2[self.current_p2]
                self.battle_log.append(f"   🔄 Player 2 sends out {next_pokemon.name}!")
                return True
            return False
    
    def is_battle_over(self) -> bool:
        """Check if battle has ended"""
        team1_alive = any(p.is_alive() for p in self.team1)
        team2_alive = any(p.is_alive() for p in self.team2)
        
        if not team1_alive:
            self.winner = "Player 2"
            return True
        elif not team2_alive:
            self.winner = "Player 1"
            return True
        
        return False
    
    def get_team_status(self, team: List[Pokemon]) -> str:
        """Get formatted status of a team"""
        status = []
        for i, pokemon in enumerate(team):
            hp_pct = pokemon.get_hp_percentage()
            active = "⭐" if ((team == self.team1 and i == self.current_p1) or 
                             (team == self.team2 and i == self.current_p2)) else "  "
            
            if pokemon.is_fainted:
                status.append(f"{active} {pokemon.name}: 💀 FAINTED")
            else:
                hp_bar = self._create_hp_bar(hp_pct)
                status.append(f"{active} {pokemon.name}: {hp_bar} {pokemon.current_hp}/{pokemon.max_hp} HP")
        
        return "\n".join(status)
    
    def _create_hp_bar(self, percentage: float, length: int = 10) -> str:
        """Create a visual HP bar"""
        filled = int(percentage / 10)
        empty = length - filled
        
        if percentage > 50:
            color = "🟩"
        elif percentage > 25:
            color = "🟨"
        else:
            color = "🟥"
        
        return color * filled + "⬜" * empty
    
    def get_battle_summary(self) -> Dict:
        """Get summary of the battle"""
        return {
            'turns': self.turn_number,
            'winner': self.winner,
            'team1_remaining': sum(1 for p in self.team1 if p.is_alive()),
            'team2_remaining': sum(1 for p in self.team2 if p.is_alive()),
            'battle_log': self.battle_log
        }


def simulate_auto_battle(team1: List[Dict], team2: List[Dict], max_turns: int = 50) -> Dict:
    """Simulate a full auto battle and return results"""
    battle = BattleEngine(team1, team2)
    
    while not battle.is_battle_over() and battle.turn_number < max_turns:
        battle.execute_turn()
    
    if battle.turn_number >= max_turns:
        battle.winner = "Draw (Time Limit)"
    
    return battle.get_battle_summary()
