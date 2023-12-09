"use client";
import {
  Button,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverArrow,
  PopoverHeader,
  PopoverCloseButton,
  PopoverBody,
  PopoverFooter,
} from '@chakra-ui/react';

export default function Logout(){
    const handleLogout = () => {
        localStorage.removeItem("token");
        window.location.href="./"
    }

    return (
        <Popover>
          <PopoverTrigger>
            <Button 
                fontWeight="bold" 
                color={"#134074"}
                _hover={{
                    color:'#3FC3FE',
                }}
                variant={"ghost"}
                >Logout</Button>
          </PopoverTrigger>
          <PopoverContent>
            <PopoverArrow />
            <PopoverHeader fontWeight="bold">Logout</PopoverHeader>
            <PopoverCloseButton />
            <PopoverBody>
              Are you sure want to logout?<br/><br/>
              <Button
                backgroundColor="#134074"
                color={"#FFFFFF"}
                _hover={{
                    bgColor:'#3FC3FE',
                }}
                onClick={handleLogout}>
                Yes
              </Button>
            </PopoverBody>
          </PopoverContent>
        </Popover>
      );
}