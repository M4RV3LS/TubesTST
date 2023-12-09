"use client";

import {
    Box,
    useBreakpointValue,
    Image,
    VStack,
    Input,
    Button,
    AlertIcon,
    Alert,
    FormControl,
    Heading,
    Text,
    HStack
  } from "@chakra-ui/react";
import { useState } from "react";
import '@fontsource/cinzel';
import axios from "axios";

export default function Login(){
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    async function handleLogin(event: React.FormEvent<HTMLFormElement>) {
        event.preventDefault();
    
        try {
          const response = await axios.post(
            "http://127.0.0.1:8000/token",
            new URLSearchParams({
              username: username,
              password: password,
            }),
            {
              headers: {
                "Content-Type": "application/x-www-form-urlencoded",
                Authorization: `Bearer ${localStorage.getItem("token")}`
              },
            }
          );

          const token = response.data.access_token;
          localStorage.setItem("token", token);
          console.log("Login successful", response.data);
          window.location.href = "./home";
        } catch (error) {
          console.error("Login error:", error);
        }
      }
    
      return(
        <VStack
          bgColor={'#FFFFFF'}
          minWidth={"500px"}
          height={"100vh"}
          justifyContent={"center"}
          spacing={"20px"}
          color={'#134074'}
        >
          <Image src={"./logo.png"} height={"150px"} />
          <Heading fontFamily={'cinzel'} fontSize={'xx-large'}>Login</Heading>
          <form onSubmit={handleLogin}>
            <VStack spacing={'1px'}>
                <Input
                type="username"
                id="username"
                size="md"
                variant={"filled"}
                placeholder="Username"
                name="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                p={10}
                border={'1px solid #134074'}
                borderRadius={'20px'}
                required
                ></Input>
                <Input
                type="password"
                id="password"
                mt="20px"
                size="md"
                variant={"filled"}
                placeholder="Password"
                name="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                p={10}
                border={'1px solid #134074'}
                borderRadius={'20px'}
                required
                ></Input>
                <Button
                    mt={'12px'}
                    px={'65px'}
                    pt={8}
                    pb={8}
                    bgColor="#134074"
                    color="white"
                    _hover={{ bg: '#3FC3FE' }}
                    fontWeight={'bold'}
                    borderRadius={30}
                    mx={1}
                    type="submit"
                >
                    Login
                </Button>
            </VStack>
          </form>
          <HStack>
            <Text>Don't have an account?</Text>
            <Button
                variant='link'
                _hover={{
                    color:'#3FC3FE',
                    borderBottom: '1px solid #3FC3FE',
                }}
                borderBottom={'1px solid #134074'}>
                <a href="./register">Register here!</a>
            </Button>
          </HStack>
        </VStack>
      )
}
