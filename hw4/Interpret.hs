---------------------------------------------------------------------
-- Name: Hwa-seung Erstling (U36770098)
-- CAS CS 320, Fall 2015
-- Assignment 4
-- Interpret.hs
-- 

type Value = Integer
type Output = [Value]

data Term =
    Number Integer
  | Plus Term Term
  | Mult Term Term
  | Exponent Term Term
  | Max Term Term
  | Min Term Term
  deriving (Eq, Show);

data Stmt =
    Print Term Stmt
  | End
  deriving (Eq, Show);
  
evaluate :: Term -> Value
evaluate (Number i) = i
evaluate (Plus t1 t2) = evaluate(t1) + evaluate(t2)
evaluate (Mult t1 t2) = evaluate(t1) * evaluate(t2)
evaluate (Exponent t1 t2) = evaluate(t1) ^ evaluate(t2)
evaluate (Max t1 t2) = max (evaluate(t1)) (evaluate(t2))
evaluate (Min t1 t2) = min (evaluate(t1)) (evaluate(t2))

execute :: Stmt -> Output
execute (End) = []
execute (Print t1 s1) = [evaluate(t1)] ++ execute(s1)

--eof