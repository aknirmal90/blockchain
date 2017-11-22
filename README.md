`python app.py`
Runs a light-weight node made available via Flask webserver

Available endpoints are

i)    /chain/list - GET
   retrieves a list of blocks which makes up the blochain on the current node.
ii)  /transaction/new - POST
   submits a new transaction to be added to the current node's blockchain when the next block mined.
iii) /mine - POST
   instructs the node to mine the next block
iv)  /node/register - POST
   submits a list of active nodes on the blockchain network
v)   /node/resolve - POST
   attempts to identify the longest chain on the network and replaces the chain on the current node with the longest chain.
   
You will need atleast 2 nodes to attempt /node/resolve
