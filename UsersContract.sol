pragma solidity ^0.6.8;

contract UsersContract {
    User[] public users;

    uint256 userCount;

    struct User {
        string _account;
        string _hash_image;
    }

    function addUser(string memory _account, string memory _hash_image) public {
        users.push(User(_account, _hash_image));
        userCount += 1;
    }

    function getUserCount()public view returns(uint256){
        return userCount;
    }

    function getUser(uint256 index) view public  returns (string memory, string memory){
        return (users[index]._account, users[index]._hash_image);
    }
}
