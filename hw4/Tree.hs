---------------------------------------------------------------------
-- Name: Hwa-seung Erstling (U36770098)
-- CAS CS 320, Fall 2015
-- Assignment 4 (skeleton code)
-- Tree.hs
--
--module Tree where

data Tree =
    Leaf
  | Twig
  | Branch Tree Tree Tree
  deriving (Eq, Show);
  
twigs :: Tree -> Integer
twigs (Leaf) = 0
twigs (Twig) = 1
twigs (Branch t1 t2 t3) = twigs(t1) + twigs(t2) + twigs(t3)

branches :: Tree -> Integer
branches (Leaf) = 0
branches (Twig) = 0
branches (Branch t1 t2 t3) = 1 + branches(t1) + branches(t2) + branches(t3)

width :: Tree -> Integer
width (Leaf) = 1
width (Twig) = 1
width (Branch t1 t2 t3) = width(t1) + width(t2) + width(t3)

perfect :: Tree -> Bool
perfect (Leaf) = True
perfect (Twig) = False
perfect (Branch Leaf Leaf Leaf) = True
perfect (Branch t1 t2 t3) = perfect(t1) && perfect(t2) && perfect(t3) && t1 == t2 && t2 == t1 

weight (Leaf) = 1
weight (Twig) = 1
weight (Branch t1 t2 t3) = 0

degenerate :: Tree -> Bool
degenerate (Leaf) = True
degenerate (Twig) = True
degenerate (Branch Leaf Leaf Leaf) = True
degenerate (Branch t1 t2 t3) = (weight(t1)+weight(t2)+weight(t3) >= 2) && degenerate(t1) && degenerate(t2) && degenerate(t3)

infinite :: Tree
infinite = Branch Leaf infinite Leaf


--eof