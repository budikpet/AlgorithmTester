.. _SlackClient: https://github.com/slackapi/python-slackclient

Algorithm tester
===================
Click CLI aplikace pro testování vlastností algoritmů. Aplikaci jsou zadány instance problému ve vstupních souborech, výstupem jsou soubory se zpracováním těchto instancí pomocí zadaných algoritmů.

Aplikace musí umožňovat řešení různých algoritmických problémů (např. Knapsack Problem, SAT). Instance těchto problémů jsou odlišné a formáty vstupních souborů mohou být odlišné, aplikace používá parser pro čtení těchto instancí ze souborů. Aplikace musí umožňovat přidání konkrétních parserů formou pluginů.

Aplikace musí umožňovat přidání nových testovaných algoritmů formou pluginů.

Použití
---------

Aplikace ze složky čte soubory s instancemi problému, která předává požadovaným algoritmům.
Algoritmy instance zpracují, výsledky jsou postupně zapisovány do výstupní složky do souborů.

Pokud v některém z algoritmů dojde při vyhodnocování k chybě, nebude ovlivněno vyhodnocování ostatních algoritmů.

Ukázka Click CLI interface:
_____________________________

+-------------------------+----------+-----------------------------------------------------------------------------+--------------------------------------------+
| **Option**              | **Type** | **Info**                                                                    | **Default**                                |
+-------------------------+----------+-----------------------------------------------------------------------------+--------------------------------------------+
| **-s, --algorithms**    | TEXT     | CSV string of names of available algorithms.                                | Example: Brute, DynamicProgramming, Greedy |
+-------------------------+----------+-----------------------------------------------------------------------------+--------------------------------------------+
| **-p, --parser**        | TEXT     | Name of the parser that is used to parse input files.                       | Example: KnapsackBaseParser                |
+-------------------------+----------+-----------------------------------------------------------------------------+--------------------------------------------+
| **-c, --communicators** | TEXT     | CSV string of names of available communication interfaces.                  |                                            |
+-------------------------+----------+-----------------------------------------------------------------------------+--------------------------------------------+
| **--check-time**        | BOOLEAN  | Should the result check real elapsed time.                                  | False                                      |
+-------------------------+----------+-----------------------------------------------------------------------------+--------------------------------------------+
| **-f, --force**         | BOOLEAN  | If True then rewrites all already present output files as the program runs. | False                                      |
|                         |          |                                                                             |                                            |
|                         |          | If False then the program continues where it left off.                      |                                            |
+-------------------------+----------+-----------------------------------------------------------------------------+--------------------------------------------+

+----------------+-------------------+--------------------------------------------------------------------------+
| **Argument**   | **Type**          | **Help**                                                                 |
+----------------+-------------------+--------------------------------------------------------------------------+
| **INPUT_DIR**  | Path to directory | Directory with input files that are to be parsed using a defined parser. |
+----------------+-------------------+--------------------------------------------------------------------------+
| **OUTPUT_DIR** | Path to directory | Directory where output files are stored.                                 |
+----------------+-------------------+--------------------------------------------------------------------------+

Použité knihovny
-------------------

- Click CLI
- Numpy

  - použito v jednotlivých prověřovaných algoritmech
- Generátorové funkce
- AsyncIO
- Pandas

  - zpracování výsledků v Jupyter notebooku
  - notebooky jsou součástí repository, ale samotný script pro ně pouze generuje výsledky

Přidání nových algoritmů
----------------------------

Nové algoritmy pro testování lze aplikaci předat prostřednictvím pluginů. Každý z těchto algoritmů musí být dědicem třídy Algorithm. Aplikace pracuje pouze s metodami třídy Algorithm.

Zjednodušená třída Algorithm:
________________________________

.. code-block:: python

  class Algorithm(object):
      def get_name(self) -> str:
          pass
     def perform_algorithm(self, parsed_data) -> str:
          pass

Propojení s komunikačním rozhraním
=====================================

Protože zpracování instancí může trvat velmi dlouho, může aplikace posílat události s informacemi o stavu zpracování. Způsoby komunikace jsou rozšiřitelné formou pluginů. Je možné současně použít 0..* způsobů komunikace zároveň.

Využití:
__________

- Zobrazení, kolik již bylo zpracováno souborů
- Možnost stáhnout obsah složky s výstupními soubory

Výchozím způsobem komunikace je Slack kanál, ke kterému se aplikace připojuje pomocí SlackClient_.
