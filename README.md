# seuRTS
microRTS project from SEU


1. Run sock/ServerAI.py 
 
2. Run microrts/src/tests/sockets/RunClientExample.java
  
  You can also:
  1. Run microrts/src/tests/sockets/RunServerExample.java
  2. Run microrts/src/tests/sockets/RunClientExample.java

to see the illustrative running example of this server.


# What you should go through

Main file to look at is sock/Sever.py

Focus on SeverAI.py and don't pay attention to SocketAI.py, nor hardCodedJSON.py


Methods you should look at are:

      BabyAI.getAction(player, gs)
      policy(player, gs)

Currently, policy always returns "Do nothing until be killed."

For the details "parameter" and "type" in the return dict of 
policy, please check hardCodedJSON.py

# What you can modify or contribute

## Modifications you can do
We almost have everything for RL problem, so that once you can format
out the environment and agents from ''gs'', you should be able to interact with the clients example.

Modify the policy function to change the responses of BabyAI.

## Contributions you can do
1. **preGameAnalysis** part in Server.py has been barely done, please do contribution to this part if you can.
2. **hardCodedJSON** has not been modified to support any else mode but fully-observed & deterministic mode. 
3. ...


# Problems
**1. How to define reward?**

⋅⋅⋅In RL problem, we always see the transition pairs like (S_t, a, r, S_t+1)
    


  
  
 

  

