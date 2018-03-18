//! # Combustion
//!
//! `libcombustion_r` is a library that will allow you convert a Halo PC map to
//! work with Halo CE.


/// This is the function that is exposed by the compiled library that will convert a map.
///
/// See the "examples" folder for using this with Python3.
///
/// # Arguments
///
/// * `buffer` - @todo - the buffer to write the converted map data to
/// * `buffer_len` - @todo - should this always be passed as zero?
/// * `map_data_raw` - @todo - the buffer for the Halo PC map file
/// * `map_data_len` - the number of bytes in the `map_data_raw` buffer
/// * `multiplayer_raw` - @todo - ???
/// * `multiplayer_len` - @todo - the number of bytes in the `multiplayer_raw` buffer
/// * `bitmaps_pc_raw` - @todo - the buffer for the Halo PC bitmaps.map file
/// * `bitmaps_pc_len` - the number of bytes in the `bitmaps_pc_raw` buffer
/// * `bitmaps_ce_raw` - @todo - the buffer for the Halo CE bitmaps.map file
/// * `bitmaps_ce_len` - the number of bytes in the `bitmaps_ce_raw` buffer
/// * `sounds_pc_raw` - @todo  - the buffer for the Halo PC sounds.map file
/// * `sounds_pc_len` - the number of bytes in the `sounds_pc_raw` buffer
/// * `sounds_ce_raw` - @todo - the buffer for the Halo CE sounds.map file
/// * `sounds_ce_len` - the number of bytes in the `sounds_ce_raw` buffer


#[no_mangle]
pub unsafe extern "C" fn testmebro(
    a: usize,
    b: usize,
    c: usize,
    d: usize,
    e: usize,
    f: usize,
    g: usize,
    h: usize,
    i: usize,
    j: usize,
) -> usize {
    println!("a: {}", a);
    println!("b: {}", b);
    println!("c: {}", c);
    println!("d: {}", d);
    println!("e: {}", e);
    println!("f: {}", f);
    println!("g: {}", g);
    println!("h: {}", h);
    println!("i: {}", i);
    println!("j: {}", j);

    0
}
