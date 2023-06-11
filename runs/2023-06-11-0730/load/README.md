# Small Concert Scenario
The small concert scenario should purchase approximately 600 tickets.
The scenario performs a 'login' by querying the /users endpoint, then purchases a ticket, then tries to view the ticket.
There will be some variance in the number of tickets attempted to be purchased based on how performant the service is.

747 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.


# Pre-Sale for Hamilton Scenario
The presale scenario should purchase approximately 1100 tickets.
The scenario is similar to the small concert scenario, but with more users.

1256 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.


# General Sale for Hamilton Scenario
The general sale scenario should purchase approximately 6000 tickets.
The scenario is similar to the small concert and pre-sale scenarios, but with even more users.
The capacity of the concert is 3000 tickets so only 3000 purchases should be successful.

8764 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.


# Seating Plan Launch Scenario
The seating plan launch scenario should purchase approximately 5500 tickets.
At the same time there will be 5 parallel event staff trying to view the seating plan a total of 50 times.
The concert has a maximum capacity of 3000 seats so there should only be 3000 successful purchases.

8762 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.
50 attempts to view the seating plan.
0 successful seating plan views.


# Evening Shows at QPAC Scenario
In this scenario, there are 3 concerts with tickets being purchased at different rates concurrently.
The approximate amount of purchases are 600, 800, and 900 respectively.
The capacities of the concerts are 3000, 2000, and 1500 respectively.
There will also be 5 parallel staff generating a total of 50 seating plans across the 3 concerts.

## Concert 1
3660 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.

## Concert 2
2971 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.

## Concert 3
1410 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.

## Staff
50 attempts to view the seating plan.
0 successful seating plan views.


# Priority Tickets Scenario
In this scenario, there are 2 concerts, one in a year and one today.
The concert next year attempts to purchase and print approximately 1700 tickets.
The concert today attempts to purchase and print exactly 50 tickets.
The concert today should successfully print all tickets despite the load on the concert in a year.
The concert next year does not have to successfully print all tickets.

## Today's Concert
50 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.

50 attempts to print a ticket.
50 successful ticket prints.

## Next Year's Concert
2971 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.

2971 attempts to print a ticket.
2971 successful ticket prints.


# Copyright Scenario
In this scenario, there is one concert (capacity 3000), initially named Elsa on Ice.
In the first 30 seconds, 1000 tickets are purchased.
Then the concert name is changed to Bob on Ice.
We then try to reprint 20 tickets, ensuring that the name change is reflected on the tickets.

15 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.

20 attempts to reprint tickets.
0 successful reprints.


# Taylor Swift Scenario
In this scenario, there are 24 concerts. Tickets are randomly purchased from each concert.
Ticket purchasers gradually increase to around 20,000 purchases.

48355 attempts to purchase tickets.
0 successful logins.
0 successful purchases.
0 successful ticket views.


