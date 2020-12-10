import matplotlib.pyplot as plt

n_clients = [1, 2, 3, 4, 5, 6, 7] #For zzzz 30
rtt_clients = [14.387215069000376, 7.632594697002787, 7.439556156001345, 7.710962321005354, 7.693395203001273, 7.7196952949962, 7.6518684690017835]

n_clients_2 = [1,2,3,4,5,6,7] #For zzzz 1000
rtt_clients_2 = [25.816721768998832, 12.802075258994591, 9.44431288499618, 8.124007355996582, 8.33381251100218, 8.025221555995813, 8.024173834994144]

n_chars = [1,2,3,4,5] #With 5 workers and 1000 divisions
rtt_clients_3 = [0.2867302400045446, 0.3088054959953297, 0.8833679849994951, 8.02906423099921, 456.1266496990065]

plt.plot(n_clients, rtt_clients)
plt.title('Plot for number of clients vs RTT dividing ranges into 30 chunks')
plt.xlabel('Number of Clients')
plt.ylabel('RTT')
plt.savefig('./images/rtt_1.png')
plt.close()

plt.plot(n_clients, rtt_clients_2)
plt.title('Plot for number of clients vs RTT dividing ranges into 1000 chunks')
plt.xlabel('Number of Clients')
plt.ylabel('RTT')
plt.savefig('./images/rtt_2.png')
plt.close()

plt.plot(n_chars, rtt_clients_3)
plt.title('Plot for number of characters vs RTT (1000 chunks)')
plt.xlabel('Number of Characters')
plt.ylabel('RTT')
plt.savefig('./images/rtt_3.png')
plt.close()