Set Implicit Arguments.

Lemma a : forall X Y:bool,
orb (orb (negb(andb X Y)) (andb (negb X) Y)) (andb (negb X) (negb Y)) = orb (negb X) (negb Y).
Proof.
  intros a b.
  destruct a.
  + simpl. 
  destruct b.
  - simpl. reflexivity. 
  - simpl. reflexivity.
  + simpl. reflexivity.
Qed.

Lemma b : forall X Y Z:bool,
andb (andb (negb(andb (andb (negb X) Y) (negb Z))) (negb (andb(andb X Y) Z))) (andb (andb X (negb Y)) (negb Z)) = andb (andb X (negb Y)) (negb Z).
Proof.
intros a b c.
destruct a.
+ destruct b.
- destruct c.
* reflexivity.
* reflexivity.
- destruct c.
* reflexivity.
* reflexivity.
+ destruct c.
* destruct b.
- reflexivity.
- reflexivity.
* destruct b.
- reflexivity.
- reflexivity. 
Qed.