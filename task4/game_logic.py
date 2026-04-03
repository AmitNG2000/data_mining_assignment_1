"""
Game logic and validation for SQL Learning Game.
Defines Level and Challenge classes, query validation, and progress tracking.
"""
import pandas as pd
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, field
from task4.database import execute_query, execute_write_query


@dataclass
class Challenge:
    """Represents a single SQL challenge within a level."""
    question: str
    expected_result: pd.DataFrame = field(default=None, repr=False)
    expected_query: str = ""  # Example solution (for hints)
    hint_1: str = ""  # Gentle hint
    hint_2: str = ""  # More specific hint
    hint_3: str = ""  # Direct hint (almost gives away answer)
    allows_write: bool = False  # True for Level 5 INSERT/UPDATE challenges
    
    def validate_answer(self, user_query: str) -> Tuple[bool, str, Optional[pd.DataFrame]]:
        """
        Validate a user's SQL query against the expected result.
        
        Args:
            user_query: The SQL query submitted by the user
        
        Returns:
            Tuple of (is_correct, message, result_df)
        """
        try:
            # Clean the query
            user_query = user_query.strip()
            
            if not user_query:
                return (False, "❌ Please enter a SQL query.", None)
            
            # Check if write operations are allowed
            query_upper = user_query.upper()
            is_write_query = any(keyword in query_upper.split() for keyword in ['INSERT', 'UPDATE', 'DELETE'])
            
            if is_write_query and not self.allows_write:
                return (False, "❌ Only SELECT queries are allowed in this level. Try reading data, not modifying it!", None)
            
            # Execute the query
            if self.allows_write:
                # For write queries (Level 5), execute and check success
                success, message, rows_affected = execute_write_query(user_query)
                if success:
                    # For sabotage challenges, any successful write is a win
                    return (True, f"✅ {message} Sabotage successful! 😈", None)
                else:
                    return (False, f"❌ {message}", None)
            else:
                # For SELECT queries, compare results
                result_df = execute_query(user_query)
                
                if result_df is None:
                    return (False, "❌ Query failed to execute. Check your SQL syntax.", None)
                
                # Compare with expected result
                if self.expected_result is not None:
                    if self._results_match(result_df, self.expected_result):
                        return (True, "✅ Correct! Well done!", result_df)
                    else:
                        return (False, "❌ Query executed, but the result doesn't match what we expected. Try again!", result_df)
                else:
                    # No expected result to compare (open-ended challenge)
                    return (True, "✅ Query executed successfully!", result_df)
        
        except Exception as e:
            return (False, f"❌ Error: {str(e)}", None)
    
    def _results_match(self, df1: pd.DataFrame, df2: pd.DataFrame) -> bool:
        """
        Compare two DataFrames for equality (ignoring column order and index).
        
        Args:
            df1: First DataFrame
            df2: Second DataFrame
        
        Returns:
            bool: True if DataFrames contain the same data
        """
        try:
            # Check if same number of rows and columns
            if df1.shape != df2.shape:
                return False
            
            # Sort columns alphabetically for comparison
            df1_sorted = df1.sort_index(axis=1)
            df2_sorted = df2.sort_index(axis=1)
            
            # Reset index for comparison
            df1_sorted = df1_sorted.reset_index(drop=True)
            df2_sorted = df2_sorted.reset_index(drop=True)
            
            # Compare values (allowing for small floating point differences)
            return df1_sorted.equals(df2_sorted) or df1_sorted.compare(df2_sorted).empty
            
        except Exception:
            return False
    
    def get_hint(self, attempt_number: int) -> str:
        """
        Get progressively more specific hints based on attempt number.
        
        Args:
            attempt_number: Number of failed attempts (1, 2, 3+)
        
        Returns:
            str: Hint text
        """
        if attempt_number == 1 and self.hint_1:
            return f"💡 **Hint 1:** {self.hint_1}"
        elif attempt_number == 2 and self.hint_2:
            return f"💡 **Hint 2:** {self.hint_2}"
        elif attempt_number >= 3 and self.hint_3:
            return f"💡 **Hint 3:** {self.hint_3}"
        else:
            return "💡 Try reviewing the SQL concepts for this level, or check the example solution."


@dataclass
class Level:
    """Represents a complete level with story and challenges."""
    number: int
    title: str
    story_intro: str  # Story text shown before challenges
    story_outro: str = ""  # Story text shown after completing all challenges
    challenges: List[Challenge] = field(default_factory=list)
    teaches_concepts: List[str] = field(default_factory=list)  # SQL concepts taught
    
    def add_challenge(self, challenge: Challenge):
        """Add a challenge to this level."""
        self.challenges.append(challenge)
    
    def get_progress(self, completed_challenges: List[int]) -> Tuple[int, int]:
        """
        Get completion progress for this level.
        
        Args:
            completed_challenges: List of completed challenge indices
        
        Returns:
            Tuple of (completed_count, total_count)
        """
        return (len(completed_challenges), len(self.challenges))
    
    def is_complete(self, completed_challenges: List[int]) -> bool:
        """Check if all challenges in this level are complete."""
        return len(completed_challenges) == len(self.challenges)


class GameState:
    """Manages the overall game state and progress."""
    
    def __init__(self):
        self.current_level = 1
        self.completed_levels: List[int] = []
        self.level_progress: Dict[int, List[int]] = {}  # level_num -> list of completed challenge indices
        self.attempt_counts: Dict[str, int] = {}  # challenge_id -> attempt count
    
    def get_current_challenge_index(self, level_num: int) -> int:
        """Get the index of the next incomplete challenge in a level."""
        completed = self.level_progress.get(level_num, [])
        return len(completed)
    
    def mark_challenge_complete(self, level_num: int, challenge_index: int):
        """Mark a challenge as complete."""
        if level_num not in self.level_progress:
            self.level_progress[level_num] = []
        
        if challenge_index not in self.level_progress[level_num]:
            self.level_progress[level_num].append(challenge_index)
    
    def mark_level_complete(self, level_num: int):
        """Mark an entire level as complete."""
        if level_num not in self.completed_levels:
            self.completed_levels.append(level_num)
    
    def increment_attempt(self, challenge_id: str):
        """Increment the attempt counter for a challenge."""
        if challenge_id not in self.attempt_counts:
            self.attempt_counts[challenge_id] = 0
        self.attempt_counts[challenge_id] += 1
    
    def get_attempts(self, challenge_id: str) -> int:
        """Get the number of attempts for a challenge."""
        return self.attempt_counts.get(challenge_id, 0)
    
    def can_access_level(self, level_num: int) -> bool:
        """Check if a level can be accessed (previous level must be complete)."""
        if level_num == 1:
            return True
        return (level_num - 1) in self.completed_levels
    
    def get_overall_progress(self, total_levels: int) -> float:
        """Get overall completion percentage."""
        return (len(self.completed_levels) / total_levels) * 100 if total_levels > 0 else 0.0
    
    def reset(self):
        """Reset all game progress."""
        self.current_level = 1
        self.completed_levels = []
        self.level_progress = {}
        self.attempt_counts = {}


def validate_query_syntax(query: str) -> Tuple[bool, str]:
    """
    Basic syntax validation before executing a query.
    
    Args:
        query: SQL query string
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    query = query.strip()
    
    if not query:
        return (False, "Query is empty. Please enter a SQL query.")
    
    # Check for obviously dangerous patterns (though we're sandboxed, good practice)
    dangerous_patterns = ['DROP TABLE', 'DROP DATABASE', 'TRUNCATE']
    query_upper = query.upper()
    
    for pattern in dangerous_patterns:
        if pattern in query_upper:
            return (False, f"'{pattern}' is not allowed in this game. Let's keep things safe! 😊")
    
    # Basic SQL keyword check
    sql_keywords = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'FROM', 'WHERE', 'GROUP', 'ORDER', 'JOIN']
    has_keyword = any(keyword in query_upper.split() for keyword in sql_keywords)
    
    if not has_keyword:
        return (False, "This doesn't look like a SQL query. Make sure to use SQL keywords like SELECT, FROM, WHERE, etc.")
    
    return (True, "")


def format_query_result(df: pd.DataFrame, max_rows: int = 100) -> str:
    """
    Format a query result DataFrame for display.
    
    Args:
        df: Result DataFrame
        max_rows: Maximum rows to display
    
    Returns:
        str: Formatted result string
    """
    if df is None or df.empty:
        return "No results returned."
    
    row_count = len(df)
    display_df = df.head(max_rows)
    
    result = f"**{row_count} row(s) returned**\n\n"
    
    if row_count > max_rows:
        result += f"*(Showing first {max_rows} rows)*\n\n"
    
    return result
