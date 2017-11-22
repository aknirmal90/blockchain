`python app.py`
Runs a light-weight node made available via Flask webserver

<h3>Available endpoints are </h3>

<ol>
<li>    /chain/list - GET <br>
   retrieves a list of blocks which makes up the blochain on the current node.
</li>   
   
<li>  /transaction/new - POST <br>
   submits a new transaction to be added to the current node's blockchain when the next block mined.
</li>   

<li> /mine - POST <br>
   instructs the node to mine the next block
</li>   

<li>  /node/register - POST <br>
   submits a list of active nodes on the blockchain network
</li>   

<li>   /node/resolve - POST <br>
   attempts to identify the longest chain on the network and replaces the chain on the current node with the longest chain.
</li>   

</ol>   
You will need atleast 2 nodes to attempt /node/resolve
