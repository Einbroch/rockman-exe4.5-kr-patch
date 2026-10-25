import random,unittest
from lz10_greedy import encode
from verify_tpi_index import lz77_decompress

class Lz10GreedyTests(unittest.TestCase):
    def test_overlap_and_flag_group_boundaries(self):
        for data in [b'A'*1156,b'AB'*500,bytes(range(256))*4,bytes(range(33)),b'12345678123456789']:
            result=encode(data,output_limit=2000,stored_limit=3000)
            self.assertEqual(lz77_decompress(result,0)[0],data);self.assertEqual(len(result)%4,0)
            self.assertEqual(result,encode(data,output_limit=2000,stored_limit=3000))
    def test_output_and_stored_budget_rejections(self):
        for data,output,stored in [(b'',10,100),(b'1234',3,100),(bytes(range(50)),50,8)]:
            with self.assertRaises(ValueError):encode(data,output_limit=output,stored_limit=stored)
    def test_full4096_displacement_boundary(self):
        generator=random.Random(343);original=bytes(generator.randrange(256) for _ in range(4096));data=original+original[:18]
        result=encode(data,output_limit=len(data),stored_limit=6000)
        self.assertEqual(lz77_decompress(result,0)[0],data)
        at=4;cursor=0;distances=[]
        while cursor<len(data):
            flags=result[at];at+=1
            for bit in range(7,-1,-1):
                if cursor>=len(data):break
                if flags&(1<<bit):
                    a,b=result[at:at+2];at+=2;cursor+=(a>>4)+3;distances.append(((a&15)<<8|b)+1)
                else:at+=1;cursor+=1
        self.assertIn(4096,distances)

if __name__=='__main__':unittest.main()
