"use client";
import {
    Box,
    Flex,
    Spacer,
    Text,
    Link,
    Image,
    Button,
    HStack,
    Heading
  } from "@chakra-ui/react";
import '@fontsource/cinzel'
import Logout from "./Logout";

export default function Navbar(props: {status: boolean}){
    const isLogin = (props.status == true);
    const isNotLogin = (props.status == false);
    return(
        <HStack
          bg="#F2FBFF"
          color="#134074"
          p={1.5}
          fontSize="lg"
          fontWeight="bold"
          alignItems="center"
          justifyContent="space-between"
          width="100%"
          maxWidth="100%"
          marginX="auto"
          borderBottom={"1px solid #CBD5E0"}
        >
            <HStack>
                <Image
                    src="./logo.png"
                    alt="Logo"
                    ml={8}
                    mr={2}
                    h={12}
                    objectFit={"contain"}
                />
                <Heading
                fontFamily={'cinzel'}>
                    Delight Cook
                </Heading>
            </HStack>
            <Spacer display={{base: "none", md: "flex"}}></Spacer>
            { isNotLogin && 
                <HStack
                    mx={{base: 4, md: 7}}
                    position="relative"
                    fontWeight="bold"
                    padding= '10px'
                    style={{ whiteSpace: 'nowrap' }}
                >
                    <Button
                        fontWeight="bold" 
                        color={"#134074"}
                        _hover={{
                            color:'#3FC3FE',
                        }}
                        variant={"ghost"}
                        mx={1}
                    >
                        <a href="./menu-public">Menu</a>
                    </Button>
                    <Button
                        fontWeight="bold" 
                        color={"#134074"}
                        _hover={{
                            color:'#3FC3FE',
                        }}
                        variant={"ghost"}
                        mx={1}
                    >
                        <a href="./login">Login</a>
                    </Button>
                </HStack>
            }
            { isLogin && 
                <HStack
                    mx={{base: 4, md: 7}}
                    position="relative"
                    fontWeight="bold"
                    padding= '10px'
                    style={{ whiteSpace: 'nowrap' }}
                >
                    <Button
                        fontWeight="bold" 
                        color={"#134074"}
                        _hover={{
                            color:'#3FC3FE',
                        }}
                        variant={"ghost"}
                        mx={1}
                    >
                        <a href="./menu">Menu</a>
                    </Button>
                    <Button
                        fontWeight="bold" 
                        color={"#134074"}
                        _hover={{
                            color:'#3FC3FE',
                        }}
                        variant={"ghost"}
                        mx={1}
                    >
                        <a href="./history">History</a>
                    </Button>
                    <Button
                        fontWeight="bold" 
                        color={"#134074"}
                        _hover={{
                            color:'#3FC3FE',
                        }}
                        variant={"ghost"}
                        mx={1}
                    >
                        <Logout></Logout>
                    </Button>
                </HStack>
            }
        </HStack>
    )
}