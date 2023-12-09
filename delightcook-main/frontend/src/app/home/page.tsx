import { ChakraProvider, Heading, Image, Box, VStack, Text, AbsoluteCenter, Button } from "@chakra-ui/react";
import Navbar from "@/components/Navbar";
import '@fontsource/cinzel';
import Footer from "@/components/Footer";

export default function Menu(){
    return(
        <ChakraProvider>
            <Navbar status={true} />
            <Box
              backgroundImage={"./landing.png"}
              backgroundSize={'contain'}
              bgRepeat={'no-repeat'}
              height={0}
              pt={'26.04%'}
              position={'relative'}>
              <Box
                position="absolute"
                top="50%"
                left="5%"
                transform="translate(0, -50%)"
                textAlign="left"
                color="white"
                pr={'38%'}
              >
                <Heading
                  fontFamily={'cinzel'}
                  mb={6}
                  fontWeight={'bold'}
                  textShadow={'2px 2px 25px #134074'}
                  >
                    No Hassle, Just Full of Delight!
                </Heading>
                <Text
                display={{base: "none", md: "flex"}}
                mb={7}
                textShadow={'2px 2px 25px #134074'}>
                Embark on a culinary journey with Delight Cook, where we eliminate the hassle and elevate your kitchen experience. Our chef-inspired meal kits feature premium, fresh ingredients, bringing joy and convenience to your table. Say goodbye to mealtime stress and hello to delightful cooking. Ready to explore our menus? Click "See Menus" and indulge in the simplicity of a delicious meal. 🍽️✨
                </Text>
                <Button
                    fontWeight="bold" 
                    color={"#134074"}
                    bg={"white"}
                    _hover={{
                      outline: "3px solid #134074",
                    }}
                    rounded={'20px'}
                    width={'40%'}
                >
                    <a href="./menu">See Menus</a>
                </Button>
              </Box>
            </Box>
          <Footer />
        </ChakraProvider>
    )
}