pragma solidity ^0.6.8;

contract UsersContract {

   string public user;
   
   constructor() public {
       user = 'no existe usuario';
    }

    function setUser(string memory _user) public {
       user = _user;
    }

    function getUser() view public returns (string memory) {
        return user;
    }
}
