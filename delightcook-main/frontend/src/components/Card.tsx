import {
    Box,
    Text,
    Image,
    Spacer,
    Stack,
    Button,
    HStack,
  } from '@chakra-ui/react';
import '@fontsource/cinzel';
import { FaStar } from "react-icons/fa";
import { FaStopwatch, FaFire } from "react-icons/fa6";
import Link from 'next/link';

export interface CardProps {
    menu_items: {
        menu_id: number;
        menu_name: string;
        price: number;
        duration: number;
        calories: number;
        level: string;
        menu_url: string;
    }[],
    status: boolean,
    detail: boolean
}

export const Card: React.FC<CardProps> = ({ menu_items, status, detail }) => {
    const isLogin = (status == true);
    const isNotLogin = (status == false);
    const isNotDetail = (detail == false);
    return(
        <>
        {menu_items.map((menu) => (
            <Box
                key={menu.menu_id}
                w="400px"
                h={"auto"}
                bg={"white"}
                border={'1px solid #000'}
                borderRadius={15}
                padding={4}
                mx={25}
            >
                <Stack w={"100%"} h={"100%"} align={"left"}>
                    <Box boxSize={'auto'} w={'100%'}>
                        <Image
                            style={{ objectFit: 'cover' }}
                            src={menu.menu_url}
                            alt="Katalog menu"
                            width={'400px'}
                            height={'200px'}
                             />
                    </Box>
                    <HStack alignItems={'left'} w={'100%'} pb={4}>
                        <Box width={'100%'}>
                            <HStack align={'left'}>
                                <Text
                                    fontSize={'20px'}
                                    fontWeight={'Bold'}
                                    color="#134074"
                                    pb={1}
                                >
                                    {menu.menu_name}
                                </Text>
                                <Spacer />
                                <Text color="#134074">IDR {menu.price}</Text>
                            </HStack>
                            <HStack color={"#134074"}>
                                <FaStopwatch /><Text>{menu.duration} min</Text>
                                <FaStar /><Text>{menu.level}</Text>
                                <FaFire /><Text>{menu.calories} kcal</Text>
                            </HStack>
                        </Box>
                        <Spacer></Spacer>
                    </HStack>
                    <HStack textAlign={'center'} justifyItems={'center'}>
                        { isNotDetail && 
                            <Link href={`/menu/${menu.menu_id}`} passHref>
                                <Button
                                colorScheme="#134074"
                                color="#134074"
                                _hover={{ color: '#3FC3FE' }}
                                fontWeight={'bold'}
                                borderRadius={30}
                                mx={1}
                                variant={'outline'}
                                >
                                Details
                                </Button>
                            </Link>
                        }
                        { isLogin && 
                            <Button
                            bgColor="#134074"
                            color="white"
                            _hover={{ bg: '#3FC3FE' }}
                            w="50%"
                            fontWeight={'bold'}
                            borderRadius={30}
                            mx={1}
                            >
                            <a href="./order">Order</a>
                            </Button>
                        }
                        { isNotLogin && 
                            <Button
                            bgColor="#134074"
                            color="white"
                            _hover={{ bg: '#3FC3FE' }}
                            w="50%"
                            fontWeight={'bold'}
                            borderRadius={30}
                            mx={1}
                            >
                            <a href="./login">Order</a>
                            </Button>
                        }
                    </HStack>
                </Stack>
            </Box>
        ))}
        </>
    );
};
