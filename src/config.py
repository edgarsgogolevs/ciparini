COMPUTER_SLEEP = 800
DEFUALT_STARTING_NUMS = "31254"

RULES = """
  Spēles sākumā izvēlas skaitļu virkni (no 3 līdz 10 simboliem)
  un katram spēlētājam ir 0 punktu.
  Spēlētāji izpilda gājienus pēc kārtas, gājiena laikā veicot
  divu blakus stāvošu skaitļu aizvietošanu,
  pamatojoties uz šādiem principiem:
  a) ja divu blakus stāvošu skaitļu summa ir lielāka par 7,
  tad šos skaitļus aizvieto ar 1 un spēlētāja punktu skaitam pieskaita 1 punktu,
  b) ja divu blakus stāvošu skaitļu summa ir mazāka par 7,
  tad šos skaitļus aizvieto ar 3 un no spēlētāja punktu skaita atņem 1 punktu,
  un c) ja divu blakus stāvošu skaitļu summa ir vienāda ar 7,
  tad skaitļus aizvieto ar 2 un spēlētāja punktu skaitam pieskaita 1 punktu.
  Spēle beidzas, kad virkne paliek viens skaitlis.
  Uzvar spēlētājs, kam ir vairāk punktu spēles beigās.
"""