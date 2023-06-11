# Small Concert Scenario
The small concert scenario should purchase approximately 600 tickets.
The scenario performs a 'login' by querying the /users endpoint, then purchases a ticket, then tries to view the ticket.
There will be some variance in the number of tickets attempted to be purchased based on how performant the service is.

734 attempts to purchase tickets.
734 successful logins.
734 successful purchases.
734 successful ticket views.


# Pre-Sale for Hamilton Scenario
The presale scenario should purchase approximately 1100 tickets.
The scenario is similar to the small concert scenario, but with more users.

1201 attempts to purchase tickets.
1201 successful logins.
1198 successful purchases.
1198 successful ticket views.


# General Sale for Hamilton Scenario
The general sale scenario should purchase approximately 6000 tickets.
The scenario is similar to the small concert and pre-sale scenarios, but with even more users.
The capacity of the concert is 3000 tickets so only 3000 purchases should be successful.

5801 attempts to purchase tickets.
5801 successful logins.
3001 successful purchases.
2995 successful ticket views.


# Seating Plan Launch Scenario
The seating plan launch scenario should purchase approximately 5500 tickets.
At the same time there will be 5 parallel event staff trying to view the seating plan a total of 50 times.
The concert has a maximum capacity of 3000 seats so there should only be 3000 successful purchases.

7815 attempts to purchase tickets.
7815 successful logins.
3001 successful purchases.
3001 successful ticket views.
50 attempts to view the seating plan.
0 successful seating plan views.


# Evening Shows at QPAC Scenario
In this scenario, there are 3 concerts with tickets being purchased at different rates concurrently.
The approximate amount of purchases are 600, 800, and 900 respectively.
The capacities of the concerts are 3000, 2000, and 1500 respectively.
There will also be 5 parallel staff generating a total of 50 seating plans across the 3 concerts.

## Concert 1
3489 attempts to purchase tickets.
3489 successful logins.
3000 successful purchases.
3000 successful ticket views.

## Concert 2
2817 attempts to purchase tickets.
2817 successful logins.
2000 successful purchases.
2000 successful ticket views.

## Concert 3
1322 attempts to purchase tickets.
1322 successful logins.
1322 successful purchases.
1322 successful ticket views.

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
50 successful logins.
50 successful purchases.
50 successful ticket views.

50 attempts to print a ticket.
50 successful ticket prints.

## Next Year's Concert
2809 attempts to purchase tickets.
2809 successful logins.
2000 successful purchases.
1998 successful ticket views.

2809 attempts to print a ticket.
2809 successful ticket prints.


# Copyright Scenario
In this scenario, there is one concert (capacity 3000), initially named Elsa on Ice.
In the first 30 seconds, 1000 tickets are purchased.
Then the concert name is changed to Bob on Ice.
We then try to reprint 20 tickets, ensuring that the name change is reflected on the tickets.

15 attempts to purchase tickets.
15 successful logins.
15 successful purchases.
15 successful ticket views.

20 attempts to reprint tickets.
20 successful reprints.


# Taylor Swift Scenario
In this scenario, there are 24 concerts. Tickets are randomly purchased from each concert.
Ticket purchasers gradually increase to around 20,000 purchases.

21244 attempts to purchase tickets.
21244 successful logins.
20807 successful purchases.
20352 successful ticket views.


