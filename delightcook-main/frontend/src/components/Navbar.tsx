import {
    Box,
    Flex,
    Spacer,
    Text,
    Link,
    Image,
    Button,
  } from "@chakra-ui/react";

export default function Navbar(){
    return(
        <Box
          bg="#FDB235"
          color="#02033B"
          p={4}
          fontSize="lg"
          fontWeight="bold"
          display={{ md: "flex" }}
          alignItems="center"
          justifyContent="space-between"
          width="100%"
          maxWidth="100%"
          marginX="auto"
          position="relative"
        >
            <Image
                src="./logo.png"
                alt="Logo"
                boxSize={32}
                h={12}
                objectFit={"contain"}
            />
            <Flex display={{ base: "none", md: "flex" }}>
                <Box
                    mx={10}
                    position="relative"
                    fontWeight="bold"
                    padding= '10px'
                    style={{ whiteSpace: 'nowrap' }}
                    _hover={{
                    color: 'white',
                    bgColor: '#02033B',
                    rounded: 'md',
                    }}
                >
                    <Button
                        fontWeight="bold" 
                        _hover={{
                            color: 'white',
                        }}
                    >
                        <a href="./menu">Menu</a>
                    </Button>
                    
                </Box>
            </Flex>
        </Box>
    )
}