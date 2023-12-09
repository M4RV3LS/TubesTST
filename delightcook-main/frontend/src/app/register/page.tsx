"use client";

import {
    Image,
    VStack,
    Input,
    Button,
    Heading,
    Text,
    HStack,
  } from "@chakra-ui/react";
  import { useState } from "react";
  import '@fontsource/cinzel';
  import axios from "axios";
  
  export default function Register() {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
  
    async function handleRegister(event: React.FormEvent<HTMLFormElement>) {
      event.preventDefault();

      const formData = {
        username: username,
        password: password
      };

      console.log(formData);
  
      try {
        const response = await axios.post(
          "http://127.0.0.1:8000/users",
          null,
          {
            params: {
                username: formData.username,
                password: formData.password
            }
          }
        );
  
        console.log("Registration successful", response.data);
        window.location.href = "./login";
      } catch (error) {
        console.error("Registration error:", error);
      }
    }
  
    return (
      <VStack
        bgColor={"#FFFFFF"}
        minWidth={"500px"}
        height={"100vh"}
        justifyContent={"center"}
        spacing={"20px"}
        color={"#134074"}
      >
        <Image src={"./logo.png"} height={"150px"} />
        <Heading fontFamily={"cinzel"} fontSize={"xx-large"}>
          Register
        </Heading>
        <form onSubmit={handleRegister}>
          <VStack spacing={"1px"}>
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
              border={"1px solid #134074"}
              borderRadius={"20px"}
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
              border={"1px solid #134074"}
              borderRadius={"20px"}
              required
            ></Input>
            <Button
              mt={"12px"}
              px={"65px"}
              pt={8}
              pb={8}
              bgColor="#134074"
              color="white"
              _hover={{ bg: "#3FC3FE" }}
              fontWeight={"bold"}
              borderRadius={30}
              mx={1}
              type="submit"
            >
              Register
            </Button>
          </VStack>
        </form>
        <HStack>
          <Text>Already have an account?</Text>
          <Button
            variant="link"
            _hover={{
              color: "#3FC3FE",
              borderBottom: "1px solid #3FC3FE",
            }}
            borderBottom={"1px solid #134074"}
          >
            <a href="./login">Login here!</a>
          </Button>
        </HStack>
      </VStack>
    );
  }
  